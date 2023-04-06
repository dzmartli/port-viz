import Logo from './logo'
import Device from './device'
import Form from './form'
import Indication from './indication'
import PortStatus from './port-status'
import { useEffect, useState } from "react";
import { IpFormData } from './types/types'

function App() {

    const [wsChannel, setWsChannel] = useState<WebSocket | null>(null);
    const [wsEvent, setWsEvent] = useState<MessageEvent | null>(null);
    const [detach, setDetach] = useState(false);
    const [detachSendStatus, setDetachSendStatus] = useState(false);
    const [formData, setFormData] = useState({ip: '', detach: false});
    const [deviceStatus, setDeviceStatus] = useState('disconnected');
    const [deviceModel, setDeviceModel] = useState('IOS-L2');
    const [devicePorts, setDevicePorts] = useState([]);

    // Pull form data and flip detach
    const pullFormData = (data: IpFormData) => {

        // Set connecting status
        if (!detach) {
            setDeviceStatus('connecting')
            setDeviceModel('')
        }

        // Flip detach
        setDetach(!detach);
        const updatedData = {
            ip: data.ip, 
            detach: detach
        }
        setFormData(updatedData);
    }

    // Trigger creating ws channel if form submit
    useEffect(() => {

        let ws: WebSocket;

        // Prevent default trigger
        if (formData.ip === '') {
            return
        }

        // Message handler
        const messageHandler = (event: MessageEvent) => {
            setWsEvent(event);
        }

        // Clean up
        const cleanUp = () => {
            wsChannel?.removeEventListener('message', messageHandler);
            wsChannel?.close(1000);
        }

        // Close channel if detach sended
        const closeChannel = () => {
            if (detachSendStatus) {
                cleanUp()
            }
        }

        // Create ws
        const createChannel = () => {

            if (wsChannel) {
                cleanUp()
            }
            
            ws = new WebSocket(import.meta.env.VITE_WS);
            ws.onopen = () => ws.send((JSON.stringify(formData)));
            ws.addEventListener('message', messageHandler);
            setWsChannel(ws);
        }

        createChannel()
        closeChannel()

    }, [formData])

    // Trigger for ws events
    useEffect(() => {
        
        // Prevent default trigger
        if (!wsEvent) {
            return
        }

        // Update send detach status
        const updateDetachStatus = () => {
            if (formData.detach) {
                setDetachSendStatus(true)
            }
        }

        // Handle ws send
        const handleSend = () => {
            if (wsChannel?.readyState === WebSocket.OPEN) {
                wsChannel.send((JSON.stringify(formData)));
            } else {
                setTimeout(() => {handleSend()}, 1000)
            }
        };

        // Set defaults if disconnected
        const setDefaults = () => {
            if (response.device.status === 'disconnected') {
                setDetach(false)
                setDetachSendStatus(false)
                setFormData({ip: '', detach: false})
            }
        }

        const response = JSON.parse(wsEvent.data);
        setDeviceModel(response.device.model);
        setDevicePorts(response.device.ports);
        setDeviceStatus(response.device.status);
        setDefaults()
        handleSend()
        updateDetachStatus()

    }, [wsEvent])

    return (
        <>
            <Logo />
            <Form 
                pullFormData={pullFormData}
                deviceStatus={deviceStatus} 
            />
            <Indication 
                deviceStatus={deviceStatus} 
                deviceModel={deviceModel} 
                formData={formData} 
            />
            <Device 
                deviceModel={deviceModel} 
                deviceStatus={deviceStatus} 
                formData={formData} 
            />
            <PortStatus 
                deviceModel={deviceModel} 
                devicePorts={devicePorts} 
                formData={formData} 
            />
        </>
    )
}

export default App;

import Logo from './components/logo';
import Device from './components/device';
import Form from './components/form';
import Indication from './components/indication';
import PortStatus from './components/port-status';
import { useEffect, useState } from "react";
import { IpFormData } from './types/types';

function App() {

    const [wsChannel, setWsChannel] = useState<WebSocket | null>(null);
    const [wsEvent, setWsEvent] = useState<MessageEvent | null>(null);
    const [detach, setDetach] = useState(false);
    const [detachSendStatus, setDetachSendStatus] = useState(false);
    const [formData, setFormData] = useState({ip: '', detach: false});
    const [deviceStatus, setDeviceStatus] = useState('disconnected');
    const [deviceModel, setDeviceModel] = useState('not defined');
    const [devicePorts, setDevicePorts] = useState([]);

    // Pull form data and flip detach
    const pullFormData = (data: IpFormData) => {

        // Set connecting status
        if (!detach) {
            setDeviceStatus('connecting');
            setDeviceModel('not defined');
        };

        // Flip detach
        setDetach(oldDetach => !oldDetach);
        const updatedData = {
            ip: data.ip, 
            detach: detach
        };
        setFormData(updatedData);
    };

    // Trigger creating ws channel if form submit
    useEffect(() => {

        let ws: WebSocket;

        // Prevent default trigger
        if (formData.ip === '') {
            return;
        };

        // Message handler
        const messageHandler = (event: MessageEvent) => {
            setWsEvent(event);
        };

        // Clean up
        const cleanUp = () => {
            wsChannel?.removeEventListener('message', messageHandler);
            wsChannel?.close(1000);
        };

        // Close channel if detach sended
        const closeChannel = () => {
            if (detachSendStatus) {
                cleanUp();
            }
        };

        // Create ws
        const createChannel = () => {

            if (wsChannel) {
                cleanUp();
            };
            
            ws = new WebSocket(import.meta.env.VITE_WS);
            ws.onopen = () => ws.send((JSON.stringify(formData)));
            ws.addEventListener('message', messageHandler);
            setWsChannel(ws);
        }

        createChannel();
        closeChannel();

    }, [formData]);

    // Trigger for ws events
    useEffect(() => {
        
        // Prevent default trigger
        if (!wsEvent) {
            return;
        };

        const response = JSON.parse(wsEvent.data);

        // Update send detach status
        const updateDetachStatus = () => {
            if (formData.detach) {
                setDetachSendStatus(true);
            }
        };

        // Handle ws send
        const handleSend = () => {
            if (wsChannel?.readyState === WebSocket.OPEN) {
                wsChannel.send((JSON.stringify(formData)));
            } else {
                setTimeout(() => {handleSend()}, 1000);
            }
        };

        // Set defaults if disconnected
        const setDefaults = () => {
            if (response.status === 'disconnected') {
                setDetach(false);
                setDetachSendStatus(false);
                setFormData({ip: '', detach: false});
            }
        };
        
        // Alert if status 'unknown device' or 'unknown model'
        const deviceAlert = () => {
            if (response.status === 'unknown device' ||
                response.status === 'unknown model') {
                const alertStatus = response.status;
                alert(alertStatus.charAt(0).toUpperCase() + alertStatus.slice(1));
            }
        };

        // Set data from response
        const setData = () => {
            if (deviceModel !== response.model) {
                setDeviceModel(response.model);
            }
            if (deviceStatus !== response.status) {
                setDeviceStatus(response.status);
            }
            if (devicePorts !== response.ports) {
                setDevicePorts(response.ports);
            }
        };
        
        setData();
        deviceAlert();
        setDefaults();
        handleSend();
        updateDetachStatus();

    }, [wsEvent]);

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

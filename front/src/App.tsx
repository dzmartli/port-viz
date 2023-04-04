import './App.css'
import Logo from './logo'
import Device from './device'
import Form from './form'
import Indication from './indication'
import PortStatus from './port-status'
import { useEffect, useState } from "react";
import { IpFormData } from './types/types'

function App() {
    const [wsChannel, setWsChannel] = useState<WebSocket | null>(null);
    const [detach, setDetach] = useState(false);
    const [formData, setFormData] = useState({ip: '', detach: false});
    const [deviceStatus, setDeviceStatus] = useState('disconnected');
    const [deviceModel, setDeviceModel] = useState('IOS-L2');
    const [devicePorts, setDevicePorts] = useState([]);

    // Pull form data and flip detach
    const pullFormData = (data: IpFormData) => {
        setDetach(!detach);
        const updatedData = {
            ip: data.ip, 
            detach: detach
        }
        setFormData(updatedData);
    }

    useEffect(() => {
        let ws: WebSocket;

        // Message handling
        // Send detach status after every event
        const messageHandler = (event: MessageEvent) => {
            const response = JSON.parse(event.data);
            setDeviceModel(response.device.model);
            setDevicePorts(response.device.ports);
            setDeviceStatus(response.device.status);
            ws.send((JSON.stringify(formData)));
        }

        // Close ws
        const cleanUp = () => {
            wsChannel?.removeEventListener('message', messageHandler);
            wsChannel?.close();
        }

        // Prevent default trigger
        if (formData.ip === '') {
            return
        }

        // Close ws after detach click
        if (formData.detach) {
            wsChannel ? wsChannel.onopen = () => ws.send((JSON.stringify(formData))) : console.log('ws already closed');
            cleanUp();
        }

        // Create ws
        function createChannel() {
            cleanUp();
            ws = new WebSocket(import.meta.env.VITE_WS);
            ws.onopen = () => ws.send((JSON.stringify(formData)));
            ws.addEventListener('message', messageHandler);
            setWsChannel(ws);
        }

        createChannel()

    }, [formData])

    return (
        <>
            <Logo />
            <Form pullFormData={pullFormData} />
            <Indication deviceStatus={deviceStatus} deviceModel={deviceModel} formData={formData} />
            <Device deviceModel={deviceModel} deviceStatus={deviceStatus} formData={formData} />
            <PortStatus deviceModel={deviceModel} devicePorts={devicePorts} formData={formData} />
        </>
    )
}

export default App;

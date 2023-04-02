import DeviceSVG from './assets/device.svg';
import { useEffect, useState } from "react";


function PortStatus() {

    const [deviceActive, setDeviceActive] = useState(false)
    const [deviceModel, setDeviceModel] = useState('ios')
    const [devicePorts, setDevicePorts] = useState([])


    useEffect(() => {
        const ws = new WebSocket("ws://192.168.200.2:8000/ws");
        ws.addEventListener('message', (e) => {
            const response = JSON.parse(e.data)
            setDeviceActive(response.device_status.device_active)
            setDeviceModel(response.device_status.device_model)
            setDevicePorts(response.device_status.ports)
        })
    }, [])


    return (
        <>  
            {(() => {
                switch (deviceModel) {
                case 'ios':
                    return <section className='basic-grid'>
                                <div className='device'>
                                    <img src={DeviceSVG} alt="Device svg" />
                                </div>
                            <div className={`indication ${deviceActive === true ? "on" : "off"}`}>
                            </div>
                            {devicePorts.map(({name, status}) => {
                                return (
                                    <div 
                                        className={`port-${name.toLowerCase().replace('/', '_')} 
                                        status ${status === true ? "up" : "down"}`} 
                                        key={name}>
                                        up
                                    </div>
                                )
                            })}
                            </section>
                default:
                    return <h1 className='device'>Unnown device</h1>
                }
            })()}
            
        </>
    );
    
}

export default PortStatus;
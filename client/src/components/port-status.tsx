import "../styles/test_device.css";
import { PortStatusProps } from '../types/types';
import { useEffect, useState } from "react";

function PortStatus({devicePorts, deviceModel, formData}: PortStatusProps) {

    const [portStatus, setPortStatus] = useState(<div></div>);

    useEffect(() => {

        // Port status render
        const choosePortStatus = () => {
            switch (deviceModel) {
                case 'test_model':
                    setPortStatus(<div>
                                    {devicePorts.map(({name, status}) => {
                                        return (
                                            <div 
                                                className={`status ${status === true ? "up" : "down"}`}
                                                id={`port-${name.toLowerCase().replace('/', '_')}`}
                                                key={name}>
                                                up
                                            </div>
                                        )
                                    })}
                                </div>)
                    break;
                default:
                    setPortStatus(<div></div>);
                    break;
            };
        };

        // No ports if disconnected
        const ifDetach = () => {
            if (formData.detach) {
                setPortStatus(<div></div>);
            }
        };
        
        choosePortStatus();
        ifDetach();

    }, [devicePorts, formData]);

    return (
        <>  
            {portStatus}
        </>
    );
}

export default PortStatus;
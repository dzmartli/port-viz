import nullDeviceSVG from '../assets/null_device.svg';
import testDeviceSVG from '../assets/test_device.svg';
import { DeviceProps } from '../types/types';
import { useEffect, useState } from "react";

function Device({deviceStatus, deviceModel, formData}: DeviceProps) {
    
    const [deviceSVG, setDeviceSVG] = useState(nullDeviceSVG);

    useEffect(() => {

        // Device frame switch
        const chooseSVG = () => {
            switch (deviceModel) {
                case 'test_model':
                    setDeviceSVG(testDeviceSVG);
                    break;
                default:
                    setDeviceSVG(nullDeviceSVG);
                    break;
            }
        };

        // If disconnected - grey device frame
        const ifDisconnect = () => {
            if (deviceStatus === "disconnected" || formData.detach) {
                setDeviceSVG(nullDeviceSVG);
            }
        };

        chooseSVG();
        ifDisconnect();

    }, [deviceModel, deviceStatus]);

    return (
        <>  
            <section className='basic-grid'>
                <div className='device'>
                    <img src={deviceSVG} alt="Device svg" />
                </div>
            </section>
        </>
    );
}

export default Device;
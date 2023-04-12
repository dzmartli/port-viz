import nullDeviceSVG from '../assets/null_device.svg';
import testDeviceSVG from '../assets/test_device.svg';
import { DeviceProps } from '../types/types';

function Device({deviceStatus, deviceModel, formData}: DeviceProps) {

    let deviceSVG: string;

    // Device frame switch
    switch (deviceModel) {
        case 'test_model':
            deviceSVG = testDeviceSVG;
            break;
        default:
            deviceSVG = nullDeviceSVG;
            break;
    }

    // If disconnected - grey device frame
    if (deviceStatus === "disconnected" || formData.detach) {
        deviceSVG = nullDeviceSVG;
    }

    const device = <section className='basic-grid'>
                        <div className='device'>
                            <img src={deviceSVG} alt="Device svg" />
                        </div>
                   </section>;

    return (
        <>  
            {device}
        </>
    );
}

export default Device;
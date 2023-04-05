import nullDeviceSVG from './assets/null_device.svg';
import iosL2DeviceSVG from './assets/ios-l2_device.svg';
import { DeviceProps } from './types/types';

function Device({deviceStatus, deviceModel, formData}: DeviceProps) {

    let deviceSVG: string;

    // Device frame switch
    switch (deviceModel) {
        case 'vios_l2':
            deviceSVG = iosL2DeviceSVG;
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
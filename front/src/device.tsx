import nullDeviceSVG from './assets/null_device.svg';
import iosL2DeviceSVG from './assets/ios-l2_device.svg';

function Device(props: any) {

    const status = props.deviceStatus
    const model = props.deviceModel

    let deviceSVG

    if (status === "disconnected") {
        deviceSVG = nullDeviceSVG
    } else {
        switch (model) {
            case 'ios':
                deviceSVG = iosL2DeviceSVG
                break;
            default:
                deviceSVG = nullDeviceSVG
                break;
        }
    }

    const device = <section className='basic-grid'>
                        <div className='device'>
                            <img src={deviceSVG} alt="Device svg" />
                        </div>
                   </section>;

    return (
        <>  
            <div>{device}</div>
        </>
    );
}

export default Device;
import { PortStatusProps } from './types/types'

function PortStatus({devicePorts, deviceModel, formData}: PortStatusProps) {

    let portStatus: JSX.Element;

    // Port status render
    switch (deviceModel) {
        case 'test_model':
            portStatus = <div>
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
                        </div>;
            break;
        default:
            portStatus = <div></div>
            break;
    }

    // No ports if disconnected
    if (formData.detach) {
        portStatus = <div></div>;
    }

    return (
        <>  
            {portStatus}
        </>
    );
}

export default PortStatus;
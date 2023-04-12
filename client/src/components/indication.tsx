import { IndicationProps } from '../types/types';

function Indication({deviceStatus, deviceModel, formData}: IndicationProps) {

    let indicationClassName: string = 'indication ';
    let indicationText: string;

    // Status indication
    switch (deviceStatus) {
        case 'connected':
            indicationClassName += 'connected';
            indicationText = deviceModel;
            break;
        case 'connecting':
            indicationClassName += 'connecting';
            indicationText = 'CONNECTING';
            break;
        case 'disconnected':
            indicationClassName += 'disconnected';
            indicationText = 'DISCONNECTED';
            break;
        default:
            indicationClassName += 'disconnected';
            indicationText = 'DISCONNECTED';
            break;
    }

    // Indication for detach
    if (formData.detach) {
        indicationClassName = 'indication disconnected';
        indicationText = 'DISCONNECTED';
    } 

    return (
        <>  
            <div className="info">{indicationText}</div>
            <div className={indicationClassName}></div>
        </>
    )

}

export default Indication

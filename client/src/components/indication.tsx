import { IndicationProps } from '../types/types';
import { useEffect, useState } from "react";

function Indication({deviceStatus, deviceModel, formData}: IndicationProps) {

    const [indicationClassName, setIndicationClassName] = useState('');
    const [indicationText, setIndicationText] = useState('');

    useEffect(() => {
    
        const setIndication = (status: string, text: string) => {
            setIndicationClassName(status);
            setIndicationText(text);
        };   

        // Status indication
        const chooseIndication = () => {
            switch (deviceStatus) {
                case 'connected':
                    setIndication('indication connected', deviceModel)
                    break;
                case 'connecting':
                    setIndication('indication connecting', 'CONNECTING')
                    break;
                case 'disconnected':
                    setIndication('indication disconnected', 'DISCONNECTED')
                    break;
                default:
                    setIndication('indication disconnected', 'DISCONNECTED')
                    break;
            }
        };

        // Indication for detach
        const ifDetach = () => {
            if (formData.detach) {
                setIndication('indication disconnected', 'DISCONNECTED')
            }
        };

        chooseIndication();
        ifDetach();

    }, [deviceStatus, formData]);

    return (
        <>  
            <div className="info">{indicationText}</div>
            <div className={indicationClassName}></div>
        </>
    )

}

export default Indication

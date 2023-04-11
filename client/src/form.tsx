import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { IpFormProps, IpFormData } from './types/types';

function IpForm({pullFormData, deviceStatus}: IpFormProps) {
    
    const [buttonState, setButtonState] = useState(true);
    const {
        register,
        handleSubmit,
        formState: { errors }
    } = useForm({
        mode: 'onSubmit',
        defaultValues: {
            ip: '',
            detach: false
        }
    });

    const onSubmit = (data: IpFormData) => { 
        pullFormData(data);
        setButtonState(!buttonState);
    }
    
    useEffect(() => {

        if (deviceStatus === "disconnected") {
            setButtonState(true);
        }
    
    }, [deviceStatus])

    return (
        <>
            <form onSubmit={handleSubmit(onSubmit)}>
                { errors.ip && errors.ip.type === "required" && (
                    <label className="error">IP address required.</label>
                )}
                { errors.ip && errors.ip.type === "maxLength" && (
                    <label className="error">IP address is not valid.</label>
                )}
                <input className="ip" placeholder="IP address" type="text" {
                    ...register(
                        "ip", { 
                            required: true,
                            maxLength: 14,
                            pattern: {
                                value: /^(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)){3}$/gm,
                                message: "Invalid IP address."
                            }
                        })
                } />
                <button className="connect" type="submit">{buttonState ? 'CONNECT' : 'DETACH'}</button>
            </form>
        </>
    );
}

export default IpForm;
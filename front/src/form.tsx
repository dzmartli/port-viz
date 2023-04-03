import { useState } from 'react';
import { useForm } from 'react-hook-form';

function IpForm(props: any) {
    const [buttonText, setButtonText] = useState(true)
    const {
        register,
        handleSubmit,
        formState: { errors }
    } = useForm({
        mode: 'onSubmit',
        defaultValues: {
            ip: '',
            dConnect: false
        }
    });
    
    function handleClick() {
        setButtonText(!buttonText);
    }
    
    const onSubmit = (data:Object) => props.pull(data);
    

    return (
        <>
            <form onSubmit={handleSubmit(onSubmit)}>
                { errors.ip && errors.ip.type === "required" && (
                    <label className="error">IP address required.</label>
                )}
                { errors.ip && errors.ip.type === "maxLength" && (
                    <label className="error">IP address is not valid.</label>
                )}
                <input className="ip" type="text" {
                    ...register(
                        "ip", { 
                            required: true,
                            maxLength: 14,
                            pattern: {
                                value: /^(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)){3}$/gm,
                                message: "invalid IP address"
                            }
                        })
                } />
                <button className="connect" type="submit" onClick={handleClick}>{buttonText ? 'CONNECT' : 'DISCONNECT'}</button>
            </form>
        </>
    );
}

export default IpForm;
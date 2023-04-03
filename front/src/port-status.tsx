function PortStatus(props: any) {

    return (
        <>  
           {props.devicePorts.map(({name, status}) => {
                return (
                    <div 
                        className={`port-${name.toLowerCase().replace('/', '_')} 
                        status ${status === true ? "up" : "down"}`} 
                        key={name}>
                        up
                    </div>
                )
            })}
        </>
    );
    
}

export default PortStatus;
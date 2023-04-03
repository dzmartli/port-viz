function Indication (props:any) {

    const status = props.deviceStatus
    const model = props.deviceModel

    let indicationClassName: string = 'indication '
    let indicationText: string

    switch (status) {
        case 'connected':
            indicationClassName += 'connected'
            indicationText = model
            break;
        case 'connecting':
            indicationClassName += 'connecting'
            indicationText = 'CONNECTING'
            break;
        case 'disconnected':
            indicationClassName += 'disconnected'
            indicationText = 'DISCONNECTED'
            break;
        default:
            indicationClassName += 'disconnected'
            indicationText = 'DISCONNECTED'
            break;
    }

    return (
        <>  
            <div className="info">{indicationText}</div>
            <div className={indicationClassName}></div>
        </>
    )

}

export default Indication

import './App.css'
import Logo from './logo'
import Device from './device'
import Form from './form'
import Indication from './indication'
import PortStatus from './port-status'
import { useEffect, useState } from "react";


function App() {

  const [wsChannel, setWsChannel] = useState<WebSocket | null>(null)
  const [disconnect, setDisconnect] = useState(false)
  const [formData, setFormData] = useState({ip: '', dConnect: false})
  const [deviceStatus, setDeviceStatus] = useState('disconnected')
  const [deviceModel, setDeviceModel] = useState('IOS-L2')
  const [devicePorts, setDevicePorts] = useState([])
  
  const pull_data = (data) => {
    setDisconnect(!disconnect)
    const updateData = {
      ip: data.ip, 
      dConnect: disconnect
    }
    setFormData(updateData)
  }

  useEffect(() => {
    if (formData.ip === '') {
      return
    }

    let ws: WebSocket

    const closeHandler = () => {
      console.log('close ws')
      setTimeout(createChannel, 3000);
    }
    
    const cleanUp = () => {
      ws?.removeEventListener('close', closeHandler)
      ws?.removeEventListener('message', messageHandler)
      ws?.close()
    }
    
    const messageHandler = (e: MessageEvent) => {
      const response = JSON.parse(e.data)
      setDeviceModel(response.device.model)
      setDevicePorts(response.device.ports)
      setDeviceStatus(response.device.status)
    }

    function createChannel() {
      cleanUp()
      ws = new WebSocket("ws://192.168.200.2:8000/ws")
      ws.addEventListener('close', closeHandler)
      ws.addEventListener('message', messageHandler)
      setWsChannel(ws)
      console.log(formData)
    }
    
    createChannel()
    
    //return () => {
    //  ws?.removeEventListener('close', closeHandler)
    //  ws?.close()
    //}
  }, [formData])

  return (
    <>
      <Logo />
      <Form pull={pull_data}/>
      <Indication deviceStatus={deviceStatus} deviceModel={deviceModel}/>
      <Device deviceModel={deviceModel} deviceStatus={deviceStatus}/>
      <PortStatus devicePorts={devicePorts}/>
    </>
  )
}

export default App;

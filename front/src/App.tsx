import './App.css'
import Logo from './logo'
import Device from './device'
import Form from './form'
import Indication from './indication'
import PortStatus from './port-status'
import { useEffect, useState } from "react";


function App() {

  const [deviceStatus, setDeviceStatus] = useState('disconnected')
  const [deviceModel, setDeviceModel] = useState('ios')
  const [devicePorts, setDevicePorts] = useState([])


  useEffect(() => {
      const ws = new WebSocket("ws://192.168.200.2:8000/ws");
      ws.addEventListener('message', (e) => {
          const response = JSON.parse(e.data)
          setDeviceStatus(response.device.status)
          setDeviceModel(response.device.model)
          setDevicePorts(response.device.ports)
      })
  }, [])

  return (
    <>
      <Logo />
      <Form />
      <Indication deviceStatus={deviceStatus} deviceModel={deviceModel}/>
      <Device deviceModel={deviceModel} deviceStatus={deviceStatus}/>
      <PortStatus devicePorts={devicePorts}/>
    </>
  )
}

export default App;

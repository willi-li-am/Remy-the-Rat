import './App.css';
import { remyBase64 } from './base64images.js';
import ratatouilleSign from './assets/ratatouille_sign.png';
import {useEffect, useState} from 'react'
import { io } from 'socket.io-client';

const SOCKET_SERVER_URL = 'http://localhost:5500'

function App() {
  const [data, setData] = useState([])
  useEffect(() => {
    // Connect to the Socket.IO server
    const socket = io(SOCKET_SERVER_URL);

    const sendMessage = () => {
      const socket = io(SOCKET_SERVER_URL);
      socket.emit('receive', {first_time: true});
    };

    // Listen for messages from the server
    socket.on('receive', (data) => {
      console.log('Response from server:', data);
      setData((old_data) => [...old_data, ...data])
    });

    sendMessage()

    // Clean up the socket connection when the component unmounts
    return () => {
      socket.disconnect();
    };
  }, []);
  return (
    <div className="app-wrapper">
      <div className="sign-container">
        <img src={ratatouilleSign} alt="Ratatouille Sign" className="ratatouille-sign" />
      </div>
      <div className="container">
        {data.map((item, index) => (
          <div className="card" key={index}>
            <img src={item.image} alt={`Image for ${item.question}`} />
            <div className="card-content">
              <h3>{item.question}</h3>
              <p>{item.answer}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;

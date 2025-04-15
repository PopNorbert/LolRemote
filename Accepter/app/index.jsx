import { useState, useEffect } from 'react';
import { View, Text, Button, Alert, TouchableOpacity, StyleSheet  } from 'react-native';
import io from 'socket.io-client';
export default function Index() {
  
  const [status, setStatus] = useState("Find Match")
  const [buttonColor, setButtonColor] = useState('blue')
  const [timer, setTimer] = useState(0); 
  const [timerRunning, setTimerRunning] = useState(false);
  const socket = io('http://192.168.1.129:5000');
  useEffect(() => {
    socket.on('second_icon_found', () => {
      setStatus("Accept")
      setButtonColor('red')
    });
    return () => {
      socket.disconnect();
    };
  }, []);
  useEffect(() => {
    let interval;
    if (timerRunning) {
      interval = setInterval(() => {
        setTimer(prevTimer => prevTimer + 1); 
      }, 1000);
    } else if (!timerRunning && timer !== 0) {
      clearInterval(interval); 
    }
    return () => clearInterval(interval); 
  }, [timerRunning]);
  const handlePress = () => {
    switch (status) {
      case "Find Match":
        handleFindMatch();
        break;
      case "In Queue":
        handleCancel();
        break;
      case "Accept":
        handleAccept();
        break;
      case "Accepted":
        break;
    }
  }
  const handleFindMatch = async () => {
    try {
      const response = await fetch('http://192.168.1.129:5000/find-match');

      if (response.ok) {
        const data = await response.json();
        setButtonColor('gray')
        setStatus("In Queue")
        setTimer(0); 
        setTimerRunning(true); 
      } else {
        const data = await response.json();
        setTimer(0); 
        setTimerRunning(false); 
      }
    } catch (error) {
      console.error('Error:', error);
      Alert.alert('Error', 'There was an issue connecting to the server.');
    }
  };

  const handleCancel = async () => {
    try {
      const response = await fetch('http://192.168.1.129:5000/cancel');

      if (response.ok) {
        const data = await response.json();
        setButtonColor('blue')
        setStatus("Find Match")
      } else {
        const data = await response.json();
      }
    } catch (error) {
      console.error('Error:', error);
      Alert.alert('Error', 'There was an issue connecting to the server.');
    }
  }
  const handleAccept= async () => {
    try {
      const response = await fetch('http://192.168.1.129:5000/accept');

      if (response.ok) {
        const data = await response.json();
        setButtonColor('green')
        setStatus("Accepted")
      } else {
        const data = await response.json();
      }
    } catch (error) {
      console.error('Error:', error);
      Alert.alert('Error', 'There was an issue connecting to the server.');
    }
  }


  return (
    <View style={styles.container}>
      <TouchableOpacity
        style={[styles.button, { backgroundColor: buttonColor }]}  
        onPress={handlePress}
      >
        <Text style={styles.buttonText}>{status}</Text>
      </TouchableOpacity>
      {status === 'In Queue' && (
        <Text style={styles.timerText}>{timer}s elapsed</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 10,
  },
  button: {
    paddingVertical: 15,
    paddingHorizontal: 40,
    borderRadius: 5,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonText: {
    fontSize: 20,
    color: 'white',
  },
  timerText: {
    marginTop: 20,
    fontSize: 20,
    fontWeight: 'bold',
  },
});
;


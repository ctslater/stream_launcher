import React, { Component } from 'react';
import './Launcher.css';
import StatusHeader from './StatusHeader.js';
import PodList from './PodList.js';

class Launcher extends Component {
  render() {
    return (
      <div className="Launcher">
        <StatusHeader fields={["Kafka", "Dome", "Alerts"]}/>
        <br/><br/>
        <PodList />
      </div>
    );
  }
}

export default Launcher;

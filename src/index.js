import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Launcher from './Launcher';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(<Launcher />, document.getElementById('root'));
registerServiceWorker();

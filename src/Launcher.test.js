import React from 'react';
import ReactDOM from 'react-dom';
import Launcher from './Launcher';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<Launcher />, div);
});

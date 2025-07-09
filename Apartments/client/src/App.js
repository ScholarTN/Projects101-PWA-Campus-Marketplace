import logo from './logo.svg';
//import './App.css';

import Sidebar from './components/side_bar';
import styles from './components/side_bar.module.css';
import { useState } from 'react';
import MainComponent from './components/main_component';
//import 'bootstrap/dist/css/bootstrap.min.css';


function App() {
  const [route, setRoute] = useState('welcome'); // Default route is 'welcome'
  const [apartmentsImagesId, setApartmentsImagesId] = useState('');
  const [apartmentsImagesName, setApartmentsImagesName] = useState('');
  return (
    <div className="App">
      <div style={{ display: 'flex', flexDirection: 'row', minHeight: '80vh' }}>

        <div
          className={styles.sidebar}
        >
          <Sidebar route={route} setRoute={setRoute} />
        </div>

        {/* Main Content Area */}
        <div style={{ flex: 1, padding: '20px' }} className="content">
          <MainComponent route={route} setRoute={setRoute} apartmentsImagesId = {apartmentsImagesId} setApartmentsImagesId = {setApartmentsImagesId} apartmentsImagesName={apartmentsImagesName} setApartmentsImagesName={setApartmentsImagesName}/>

          {/* You might want to render other components here based on state or routing */}
          {/* For example:
          <AddApartmentForm />
          <ApartmentList />
          */}
        </div>

      </div>
    </div>
  );
}

export default App;


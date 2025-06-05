import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import Buy from './pages/Buy';
import Sell from './pages/Sell';
import Housing from './pages/Housing';
import AddHousing from './pages/AddHousing';
import Profile from './pages/Profile';
import ItemDetail from './pages/ItemDetail';
import HousingDetail from './pages/HousingDetail';
import Messages from './pages/Messages';
import SearchResults from './pages/SearchResults';
import PrivateRoute from './components/PrivateRoute';
import { useAuth } from './context/AuthContext';

function App() {
  const { currentUser } = useAuth();

  return (
    <Router>
      <Header />
      <main>
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/buy" component={Buy} />
          <Route path="/sell" component={Sell} />
          <Route path="/housing" exact component={Housing} />
          <PrivateRoute path="/housing/add" component={AddHousing} />
          <Route path="/housing/:id" component={HousingDetail} />
          <PrivateRoute path="/profile" component={Profile} />
          <Route path="/item/:id" component={ItemDetail} />
          <PrivateRoute path="/messages" component={Messages} />
          <Route path="/search" component={SearchResults} />
        </Switch>
      </main>
      <Footer />
    </Router>
  );
}

export default App;
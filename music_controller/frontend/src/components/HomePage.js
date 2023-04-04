import React, { Component } from "react";
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";
import { BrowserRouter as Router, Switch, Route, Link, Redirect,} from "react-router-dom";
import {Button, Grid, Typography, ButtonGroup} from "@material-ui/core";

export default class HomePage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      roomCode: null,
    };

    this.clearRoomCode = this.clearRoomCode.bind(this);
  }

  async componentDidMount() { // this function gets called
    fetch('api/user-in-room')  //goes to the api endpoint user-in-room and fetches the session data, which retrieves session data from the user
    .then((response) => response.json())  
    .then((data) => {
      this.setState({   //use this data to set the session_key to the code, see api/views for implementation
      roomCode: data.code
    });
  });
  }

  renderHomePage() {
    return (
    <Grid container spacing = {3} align = "center">
      <Grid xs = {12}>
        <Typography variant = "h3" component = "h3">
          House Party
        </Typography>
      </Grid>
      <Grid xs = {12}>
        <ButtonGroup disableElevation variant = "contained" color = "primary">
          <Button color = "primary" to ="/join" component = {Link}>
            Join a Room
          </Button>
          <Button color = "secondary" to ="/create" component = {Link}>
            Create a Room
          </Button>
        </ButtonGroup>
      </Grid>
    </Grid>
    );
  }

  clearRoomCode() {
    this.setState({
      roomCode: null,
    })
  }

  render() {
    return (
      <Router>
        <Switch>
          <Route exact path="/"      //this is saying to visit the homepage and if 
            render={() => {
            return this.state.roomCode ? // if state.roomCode has a value 
            (
            <Redirect to= {`/room/${this.state.roomCode}`}/>
            ) : (
              this.renderHomePage()
            );
          }}>
          </Route>
          <Route path="/join" component={RoomJoinPage} />
          <Route path="/create" component={CreateRoomPage} />
          <Route
            path="/room/:roomCode" //colon denotes parameter in the url, React passes some properties to the component by deault
            render={(props)=>{  
              return <Room {...props} leaveRoomCallback={this.clearRoomCode}></Room> //return a room with all the props passed from the route using spread (...) operator
            }}                                                                        // then we add our own property "leaveRoomCallback", a function to clear the roomCode state
           />                                                                         
        </Switch>
      </Router>
    );
  }
}
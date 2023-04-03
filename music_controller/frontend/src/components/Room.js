import React, { Component } from "react";
import {Button, Grid, Typography} from "@material-ui/core";
import { Link } from "react-router-dom";

export default class Room extends Component {
  constructor(props) {
    super(props);
    this.state = {
      votesToSkip: 2,
      guestCanPause: false,
      isHost: false,
    };
    this.roomCode = this.props.match.params.roomCode; /// this sets the roomCode, match is the prop that stores all of the information about how we got to the component from react Router
    this.getRoomDetails()
    this.leaveButtonPressed = this.leaveButtonPressed.bind(this)
  }

  getRoomDetails() {                                                           //fetches details with this request, then returns the response in json 
    fetch('/api/get-room' + '?code=' + this.roomCode)
    .then((response)=> {  
      if (!response.ok){
        this.props.leaveRoomCallback();
        this.props.history.push("/");
      }
     return response.json();                                                    
    }).then((data) => {                                                       // then it takes this json formatted data and arrow functions to update the states
        this.setState({
          votesToSkip: data.votes_to_skip,
          guestCanPause: data.guest_can_pause,
          isHost: data.is_host,
        });
     });
  }


  leaveButtonPressed() {
    const requestOptions = {
      method: "POST",
      headers: {'Content-Type': 'application/json'},
    };
    fetch('/api/leave-room', requestOptions).then((response)=> {
      this.props.leaveRoomCallback();
      this.props.history.push('/')// sends us back to the homepage 

    })
  }
  

  render() {
    return (
        <Grid container spacing={1} align = "center" direction = "column">
          <Grid item xs ={12}>
            <Typography variant="h4" component= "h4">Code: {this.roomCode}</Typography>
          </Grid>
          <Grid item xs ={12}>
            <Typography variant="h6" component= "h6">Votes to skip: {this.state.votesToSkip}</Typography>
          </Grid>
          <Grid item xs ={12}>
            <Typography variant="h6" component= "h6"> Guest can pause: {String(this.state.guestCanPause)}</Typography>
          </Grid>
          <Grid item xs ={12}>
            <Typography variant="h6" component= "h6">Is host: {String(this.state.isHost)}</Typography>
          </Grid>
          <Grid item xs ={12}>
            <Button variant="contained" color="secondary" onClick= {this.leaveButtonPressed}> 
            Leave Room</Button>
          </Grid>
         </Grid>
    );
  }
}
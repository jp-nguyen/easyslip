import React from "react";
import Popup from "reactjs-popup";
import { useTable } from "react-table";
import './App.css';
import axios from 'axios';

class PermissionSlipPrompt extends React.Component {
  constructor(props) {
    super(props);
      this.state = {
        selectedPdfFile: null,
        selectedCsvFile: null,
      }
  }

  handleSubmit = (event) =>{
    event.preventDefault();
    const data = new FormData()
    const {selectedPdfFile, selectedCsvFile} = this.state
    data.append("permission_slip", this.state.selectedPdfFile)
    data.append("csv_file", this.state.selectedCsvFile)
    axios.post("http://localhost:5000/upload", data, { 
      // receive two    parameter endpoint url ,form data
    })
    .then(res => { // then print response status
      console.log(res.statusText)
    }).catch( err => {
      console.log("something went wrong")
    })
  }

  handleChange = (event) =>{
    // check it out: we get the evt.target.name (which will be either "email" or "password")
    // and use it to target the key on our `state` object with the same name, using bracket syntax
    this.setState({ [event.target.name]: event.target.value });
  }
  onChangeHandlerPDF = event =>{
    console.log(event.target.files)
    this.setState({
      selectedPdfFile: event.target.files[0],
    })
  }

  onChangeHandlerCSV = event => {
    console.log(event.target.files)
    this.setState({
      selectedCsvFile: event.target.files[0],
    })
  }

  render() {
    return (
      <div className="prompt">
        <form onSubmit={this.handleSubmit}>
          <label className="prompt-label" for="name">Name</label>
          <input type="text" name="name" onChange={this.handleChange}></input>
          <label className="prompt-label" for="slip">Permission Slip (PDF)</label>
          <input type="file" className="form-control" name="file" accept=".pdf" onChange={this.onChangeHandlerPDF}></input>
          <label className="prompt-label" for="emails">Emails (CSV)</label>
          <input type="file" name="emails" accept=".csv" onChange={this.onChangeHandlerCSV}></input>
          <button type="submit">submit</button>
        </form>
      </div>
    );
  }
}


class Dashboard  extends React.Component {
  constructor() {
    super();
    this.state = {
      slips: []
    }
  }

  async componentDidMount() {
    let data = await axios.get("http://localhost:5000/perm_slips").then(res => {
      const slips = res.data.slips;
      this.setState({ slips });
    })
  }

  sendStuff = (slip_id) => {
    console.log(slip_id)
    axios.get("http://localhost:5000/perm_slips/".concat(slip_id))
  }

  render(){
    const {slips} = this.state
    const items = slips.map((data, index) => {return <tr><td>document {index + 1}</td><td><button id="addBtn"  onClick={() => this.sendStuff(data._id)}>Send</button></td>
    </tr>})
    return (
      <div>
          <table>
              {items}
          </table>
          {/* <button id="addBtn" onClick={addRow}>ADD</button> */}
      </div>
  );
  }
}


function App() {
  return (
    <div>
      <Popup trigger={<button className="button">new</button>} modal>
        <PermissionSlipPrompt />
      </Popup>
      <Dashboard />
    </div>
  );
}

export default App;
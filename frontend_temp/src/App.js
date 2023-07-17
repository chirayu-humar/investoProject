import './App.css';
import {Component} from 'react'

class App extends Component {
  state = {fileToBeSent: null, isAnySent: false, data: []}

  handleFileChange = (event) => {
    const file = event.target.files[0];
    console.log(file)
    if (file && file.type === 'text/csv') {
      this.setState({
        fileToBeSent: file,
      })
    } else {
      this.setState({
        fileToBeSent: null,
      })
      alert('Please select a .csv file.');
    }
  };

  handleUpload = async () => {
    console.log("handleUpload")
    const {fileToBeSent} = this.state
    const formData = new FormData();
    formData.append('file', fileToBeSent);
    console.log(formData)
    const response = await fetch('http://localhost:8001/upload-csv', {
      method: 'POST',
      headers: {
        'Access-Control-Allow-Origin': 'http://localhost:3004',  // Replace with specific origin if needed
      },
      body: formData,
    });
    const Data = await response.json()
    console.log(Data)
    this.setState({
      isAnySent: true,
    })
  }

  bringTheSavedData = async () => {
    const {isAnySent} = this.state 
    if (isAnySent){
      console.log("bringTheSavedData")
    const response = await fetch('http://localhost:8001/saved-data', {
      method: 'GET',
      headers: {
        'Access-Control-Allow-Origin': 'http://localhost:3004',  // Replace with specific origin if needed
      },
    });
    const DataRecieved = await response.json()
    console.log(DataRecieved)
    const {data} = DataRecieved
      this.setState({
        data: data,
      })
    }
  }
  
  render(){
    console.log("render called")
    const {data} = this.state 
    return (
      <div className="App">
        <h1>upcomming</h1>
        <div>
          <input onChange={this.handleFileChange} accept=".csv" type="file" />
        </div>
        <div className="bottomDiv">
          <div>
            <button onClick={this.handleUpload} type="button">Upload Data</button>
          </div>
          <div>
            <button onClick={this.bringTheSavedData} type="button">Get data</button>
          </div>
        </div>
        <div className='detailsContainer'>
          <table>
            <thead key="heading">
            <tr>
              <th>datetime</th>
              <th>close</th>
              <th>high</th>
              <th>low</th>
              <th>open</th>
              <th>volume</th>
              <th>instrument</th>
            </tr>
            </thead>
            {
              data.map((eachItem) => (
                <tbody key={eachItem[0]}>
                <tr>
                  <td>{eachItem[0]}</td>
                  <td>{eachItem[1]}</td>
                  <td>{eachItem[2]}</td>
                  <td>{eachItem[3]}</td>
                  <td>{eachItem[4]}</td>
                  <td>{eachItem[5]}</td>
                  <td>{eachItem[6]}</td>
                </tr>
                </tbody>
              ))
            }
          </table>
        </div>
      </div>
    );
  }
}

export default App;

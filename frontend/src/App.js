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

//   onClickHandler = () => {
//    const data = new FormData()
//    data.append('file', this.state.selectedFile)
//    axios.post("http://localhost:8000/upload", data, { 
//       // receive two    parameter endpoint url ,form data
//   })
// }



  render() {
    return (
      <div className="prompt">
        <form onSubmit={this.handleSubmit}>
          {/* <label className="prompt-label" for="name">Name</label> */}
          {/* <input type="text" name="name"></input> */}
          <label className="prompt-label" for="slip">Permission Slip (PDF)</label>
          <input type="file" className="form-control" name="file" accept=".pdf" onChange={this.onChangeHandlerPDF}></input>
          <label className="prompt-label" for="emails">Emails (CSV)</label>
          <input type="file" name="emails" accept=".csv" onChange={this.onChangeHandlerCSV}></input>
          {/* <label className="prompt-label" for="due-date">Due Date</label> */}
          {/* <input type="date" name="due-date"></input> */}
          <button type="submit">submit</button>
        </form>
      </div>
    );
  }
}

class StudentTable extends React.Component {
  constructor() {
    super();
    this.columns = React.useMemo(
      () => [
        {
          Header: 'Name',
          accessor: 'name'
        },
        {
          Header: 'Signed',
          accessor: 'signed'
        },
        {
          Header: 'Due',
          accessor: 'due'
        }
      ]
    );
  }
  render() {
    return (
      <div></div>
    );
  }
}

function Table({ columns, data }) {
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({
    columns,
    data
  });

  return (
    <table {...getTableProps()}>
      <thead>
        {headerGroups.map(headerGroup => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map(column => (
              <th {...column.getHeaderProps()}>{column.render('Header')}</th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody {...getTableBodyProps()}>
        {rows.map(
          (row, i) =>
            prepareRow(row) || (
              <tr {...row.getRowProps()}>
                {row.cells.map(cell => {
                  return (
                    <td {...cell.getCellProps()}>
                      {cell.render('Cell')}
                    </td>
                  );
                })}
              </tr>
            )
        )}
      </tbody>
    </table>
  );
}

function Dashboard({ columns, data }) {
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({
    columns,
    data
  });

  return (
    <table {...getTableProps()}>
      <thead>
        {headerGroups.map(headerGroup => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map(column => (
              <th {...column.getHeaderProps()}>{column.render('Header')}</th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody {...getTableBodyProps()}>
        {rows.map(
          (row, i) =>
            prepareRow(row) || (
              <Popup trigger={
                <tr {...row.getRowProps()}>
                  {row.cells.map(cell => {
                    return (
                      <td {...cell.getCellProps()}>
                        {cell.render('Cell')}
                      </td>
                    );
                  })}
                </tr>
              } modal >
                <Table />
              </Popup>
            )
        )}
      </tbody>
    </table>
  );
}

function App() {
  const columns = React.useMemo(
    () => [
      {
        Header: 'Name',
        accessor: 'name'
      },
      {
        Header: 'Signed',
        accessor: 'signed'
      },
      {
        Header: 'Due',
        accessor: 'due'
      }
    ]
  );

  const data = [
    {
      "name": "Field Trip Permission Slip",
      "signed": "33%",
      "due": "10/30"
    },
    {
      "name": "Student-Parent Photo Consent Form",
      "signed": "100%",
      "due": "10/25"
    },
    {
      "name": "Winter 2019 Syllabus",
      "signed": "25%",
      "due": "11/5"
    }
  ];

  return (
    <div>
      <Popup trigger={<button className="button">new</button>} modal>
        <PermissionSlipPrompt />
      </Popup>
      <Dashboard columns={columns} data={data} />
    </div>
  );
}

export default App;
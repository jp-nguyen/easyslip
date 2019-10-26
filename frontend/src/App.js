import React from "react";
import Popup from "reactjs-popup";
import { useTable } from "react-table";
import './App.css';

class PermissionSlipPrompt extends React.Component {
  render() {
    return (
      <div className="prompt">
        <form>
          <label className="prompt-label" for="name">Name</label>
          <input type="text" name="name"></input>
          <label className="prompt-label" for="slip">Permission Slip (PDF)</label>
          <input type="file" name="slip" accept=".pdf"></input>
          <label className="prompt-label" for="emails">Emails (CSV)</label>
          <input type="file" name="emails" accept=".csv"></input>
          <label className="prompt-label" for="due-date">Due Date</label>
          <input type="date" name="due-date"></input>
          <button type="submit">submit</button>
        </form>
      </div>
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

  return(
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
                  return <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                })}
              </tr>
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
      <Table columns={columns} data={data} />
    </div>
  );
}

export default App;
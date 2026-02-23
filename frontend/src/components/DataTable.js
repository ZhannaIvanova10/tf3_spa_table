import React from 'react';

function DataTable({ data, onSort, sortConfig }) {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU');
  };

  const formatNumber = (num) => {
    return new Intl.NumberFormat('ru-RU').format(num);
  };

  const getSortIcon = (field) => {
    if (sortConfig.field !== field) return '↕️';
    return sortConfig.direction === 'asc' ? '↑' : '↓';
  };

  const headers = [
    { field: 'date', label: 'Дата', sortable: false },
    { field: 'title', label: 'Название', sortable: true },
    { field: 'quantity', label: 'Количество', sortable: true },
    { field: 'distance', label: 'Расстояние', sortable: true }
  ];

  return (
    <div className="table-responsive">
      <table className="table table-striped table-hover table-bordered">
        <thead className="table-dark">
          <tr>
            {headers.map(header => (
              <th 
                key={header.field}
                onClick={() => header.sortable && onSort(header.field)}
                style={header.sortable ? { cursor: 'pointer' } : {}}
              >
                {header.label} {header.sortable && getSortIcon(header.field)}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.length === 0 ? (
            <tr>
              <td colSpan="4" className="text-center py-4">
                <h5 className="text-muted">Нет данных для отображения</h5>
              </td>
            </tr>
          ) : (
            data.map(item => (
              <tr key={item.id}>
                <td>{formatDate(item.date)}</td>
                <td>{item.title}</td>
                <td className="text-end">{formatNumber(item.quantity)}</td>
                <td className="text-end">{formatNumber(item.distance)}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default DataTable;
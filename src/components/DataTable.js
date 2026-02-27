import React from 'react';

function DataTable({ items, onSort, ordering }) {
  const getSortIcon = (field) => {
    if (ordering === field) return ' ↑';
    if (ordering === `-${field}`) return ' ↓';
    return '';
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU');
  };

  const formatNumber = (num) => {
    return new Intl.NumberFormat('ru-RU').format(num);
  };

  return (
    <div className="table-responsive">
      <table className="table table-striped table-hover table-bordered">
        <thead className="table-dark">
          <tr>
            <th>Дата</th>
            <th onClick={() => onSort('name')} style={{ cursor: 'pointer' }}>
              Название{getSortIcon('name')}
            </th>
            <th onClick={() => onSort('quantity')} style={{ cursor: 'pointer' }}>
              Количество{getSortIcon('quantity')}
            </th>
            <th onClick={() => onSort('distance')} style={{ cursor: 'pointer' }}>
              Расстояние{getSortIcon('distance')}
            </th>
          </tr>
        </thead>
        <tbody>
          {items.length === 0 ? (
            <tr>
              <td colSpan="4" className="text-center py-4">
                <h5 className="text-muted">Нет данных для отображения</h5>
              </td>
            </tr>
          ) : (
            items.map(item => (
              <tr key={item.id}>
                <td>{formatDate(item.date)}</td>
                <td>{item.name}</td>
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

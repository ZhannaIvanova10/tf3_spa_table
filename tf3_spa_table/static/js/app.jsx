const { useEffect, useState } = React;

const FILTER_COLUMNS = [
  { value: 'name', label: 'Название' },
  { value: 'quantity', label: 'Количество' },
  { value: 'distance', label: 'Расстояние' },
  { value: 'date', label: 'Дата' },
];

const FILTER_CONDITIONS = [
  { value: 'eq', label: 'Равно' },
  { value: 'contains', label: 'Содержит' },
  { value: 'gt', label: 'Больше' },
  { value: 'lt', label: 'Меньше' },
];

function App() {
  const [items, setItems] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [ordering, setOrdering] = useState('name');
  const [filterColumn, setFilterColumn] = useState('name');
  const [filterCondition, setFilterCondition] = useState('contains');
  const [filterValue, setFilterValue] = useState('');

  const loadData = async (nextPage = page) => {
    const params = {
      page: nextPage,
      page_size: 10,
      ordering,
    };

    if (filterValue.trim()) {
      params.filter_column = filterColumn;
      params.filter_condition = filterCondition;
      params.filter_value = filterValue;
    }

    const response = await axios.get('/api/items/', { params });
    setItems(response.data.results);
    setPage(nextPage);
    setTotalPages(Math.max(1, Math.ceil(response.data.count / 10)));
  };

  useEffect(() => {
    loadData(1);
  }, [ordering]);

  const onFilterSubmit = (event) => {
    event.preventDefault();
    loadData(1);
  };

  const clearFilter = () => {
    setFilterValue('');
    setFilterColumn('name');
    setFilterCondition('contains');
    setTimeout(() => loadData(1), 0);
  };

  const toggleSort = (field) => {
    if (!['name', 'quantity', 'distance'].includes(field)) {
      return;
    }
    setOrdering((prev) => {
      if (prev === field) {
        return `-${field}`;
      }
      if (prev === `-${field}`) {
        return field;
      }
      return field;
    });
  };

  const getSortIcon = (field) => {
    if (ordering === field) {
      return '↑';
    }
    if (ordering === `-${field}`) {
      return '↓';
    }
    return '';
  };

  return (
    <>
      <form className="row g-2 mb-3" onSubmit={onFilterSubmit}>
        <div className="col-md-3">
          <select className="form-select" value={filterColumn} onChange={(e) => setFilterColumn(e.target.value)}>
            {FILTER_COLUMNS.map((column) => (
              <option key={column.value} value={column.value}>{column.label}</option>
            ))}
          </select>
        </div>
        <div className="col-md-3">
          <select className="form-select" value={filterCondition} onChange={(e) => setFilterCondition(e.target.value)}>
            {FILTER_CONDITIONS.map((condition) => (
              <option key={condition.value} value={condition.value}>{condition.label}</option>
            ))}
          </select>
        </div>
        <div className="col-md-4">
          <input
            className="form-control"
            value={filterValue}
            onChange={(e) => setFilterValue(e.target.value)}
            placeholder="Введите значение"
          />
        </div>
        <div className="col-md-2 d-flex gap-2">
          <button type="submit" className="btn btn-primary w-100">Применить</button>
          <button type="button" className="btn btn-outline-secondary" onClick={clearFilter}>×</button>
        </div>
      </form>

      <table className="table table-bordered table-clickable">
        <thead className="table-light">
        <tr>
          <th>Дата</th>
          <th onClick={() => toggleSort('name')}>Название <span className="sort-indicator">{getSortIcon('name')}</span></th>
          <th onClick={() => toggleSort('quantity')}>Количество <span className="sort-indicator">{getSortIcon('quantity')}</span></th>
          <th onClick={() => toggleSort('distance')}>Расстояние <span className="sort-indicator">{getSortIcon('distance')}</span></th>
        </tr>
        </thead>
        <tbody>
        {items.map((item) => (
          <tr key={item.id}>
            <td>{item.date}</td>
            <td>{item.name}</td>
            <td>{item.quantity}</td>
            <td>{item.distance}</td>
          </tr>
        ))}
        {items.length === 0 && (
          <tr>
            <td colSpan="4" className="text-center">Нет данных</td>
          </tr>
        )}
        </tbody>
      </table>

      <div className="d-flex justify-content-between align-items-center">
        <button className="btn btn-outline-primary" disabled={page <= 1} onClick={() => loadData(page - 1)}>Назад</button>
        <span>Страница {page} из {totalPages}</span>
        <button className="btn btn-outline-primary" disabled={page >= totalPages} onClick={() => loadData(page + 1)}>Вперед</button>
      </div>
    </>
  );
}

ReactDOM.createRoot(document.getElementById('app')).render(<App />);

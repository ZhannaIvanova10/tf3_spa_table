import React from 'react';

function FilterControls({ filters, setFilters, onFilter }) {
  const columns = [
    { value: 'title', label: 'Название' },
    { value: 'quantity', label: 'Количество' },
    { value: 'distance', label: 'Расстояние' }
  ];

  const conditions = [
    { value: 'exact', label: 'Равно' },
    { value: 'icontains', label: 'Содержит' },
    { value: 'gt', label: 'Больше' },
    { value: 'lt', label: 'Меньше' }
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onFilter();
  };

  const handleReset = () => {
    setFilters({
      column: 'title',
      condition: 'icontains',
      value: ''
    });
    onFilter();
  };

  return (
    <div className="card mb-4">
      <div className="card-header bg-primary text-white">
        <h5 className="mb-0">Фильтрация данных</h5>
      </div>
      <div className="card-body">
        <form onSubmit={handleSubmit}>
          <div className="row">
            <div className="col-md-3 mb-2">
              <label className="form-label">Колонка</label>
              <select 
                className="form-select"
                name="column"
                value={filters.column}
                onChange={handleChange}
              >
                {columns.map(col => (
                  <option key={col.value} value={col.value}>
                    {col.label}
                  </option>
                ))}
              </select>
            </div>
            <div className="col-md-3 mb-2">
              <label className="form-label">Условие</label>
              <select 
                className="form-select"
                name="condition"
                value={filters.condition}
                onChange={handleChange}
              >
                {conditions.map(cond => (
                  <option key={cond.value} value={cond.value}>
                    {cond.label}
                  </option>
                ))}
              </select>
            </div>
            <div className="col-md-4 mb-2">
              <label className="form-label">Значение</label>
              <input 
                type={filters.column === 'title' ? 'text' : 'number'}
                className="form-control"
                name="value"
                value={filters.value}
                onChange={handleChange}
                placeholder="Введите значение"
                required
              />
            </div>
            <div className="col-md-2 mb-2 d-flex align-items-end">
              <button 
                type="submit" 
                className="btn btn-primary w-100 me-2"
              >
                Применить
              </button>
              <button 
                type="button" 
                className="btn btn-secondary w-100"
                onClick={handleReset}
              >
                Сброс
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}

export default FilterControls;
import React from 'react';

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

function FilterControls({ 
  filterColumn, setFilterColumn,
  filterCondition, setFilterCondition,
  filterValue, setFilterValue,
  onFilter, onClear 
}) {
  return (
    <div className="card mb-4">
      <div className="card-header bg-primary text-white">
        <h5 className="mb-0">Фильтрация данных</h5>
      </div>
      <div className="card-body">
        <form onSubmit={(e) => { e.preventDefault(); onFilter(); }}>
          <div className="row g-3">
            <div className="col-md-3">
              <label className="form-label">Колонка</label>
              <select 
                className="form-select"
                value={filterColumn}
                onChange={(e) => setFilterColumn(e.target.value)}
              >
                {FILTER_COLUMNS.map(col => (
                  <option key={col.value} value={col.value}>{col.label}</option>
                ))}
              </select>
            </div>
            <div className="col-md-3">
              <label className="form-label">Условие</label>
              <select 
                className="form-select"
                value={filterCondition}
                onChange={(e) => setFilterCondition(e.target.value)}
              >
                {FILTER_CONDITIONS.map(cond => (
                  <option key={cond.value} value={cond.value}>{cond.label}</option>
                ))}
              </select>
            </div>
            <div className="col-md-4">
              <label className="form-label">Значение</label>
              <input
                type={filterColumn === 'name' || filterColumn === 'date' ? 'text' : 'number'}
                className="form-control"
                value={filterValue}
                onChange={(e) => setFilterValue(e.target.value)}
                placeholder="Введите значение"
              />
            </div>
            <div className="col-md-2 d-flex align-items-end">
              <button type="submit" className="btn btn-primary w-100">
                Применить
              </button>
            </div>
          </div>
          <div className="mt-2">
            <button type="button" className="btn btn-outline-secondary" onClick={onClear}>
              Сбросить фильтры
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
export default FilterControls;

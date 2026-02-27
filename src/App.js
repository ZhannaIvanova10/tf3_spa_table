import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import FilterControls from './components/FilterControls';
import DataTable from './components/DataTable';
import Pagination from './components/Pagination';

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

  const handleFilter = () => {
    loadData(1);
  };

  const clearFilter = () => {
    setFilterValue('');
    setFilterColumn('name');
    setFilterCondition('contains');
    setTimeout(() => loadData(1), 0);
  };

  const toggleSort = (field) => {
    if (!['name', 'quantity', 'distance'].includes(field)) return;
    setOrdering((prev) => {
      if (prev === field) return `-${field}`;
      if (prev === `-${field}`) return field;
      return field;
    });
  };

  return (
    <div className="container mt-4">
      <h1 className="mb-4 text-center">Управление таблицей</h1>
      
      <FilterControls 
        filterColumn={filterColumn}
        setFilterColumn={setFilterColumn}
        filterCondition={filterCondition}
        setFilterCondition={setFilterCondition}
        filterValue={filterValue}
        setFilterValue={setFilterValue}
        onFilter={handleFilter}
        onClear={clearFilter}
      />
      <DataTable 
        items={items} 
        onSort={toggleSort}
        ordering={ordering}
      />
      
      <Pagination 
        page={page}
        totalPages={totalPages}
        onPageChange={loadData}
      />
    </div>
  );
}

export default App;

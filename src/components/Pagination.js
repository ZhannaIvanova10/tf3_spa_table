import React from 'react';

function Pagination({ page, totalPages, onPageChange }) {
  return (
    <div className="d-flex justify-content-between align-items-center mt-4">
      <div className="text-muted">
        Страница {page} из {totalPages}
      </div>
      
      <nav>
        <ul className="pagination">
          <li className={`page-item ${page <= 1 ? 'disabled' : ''}`}>
            <button 
              className="page-link" 
              onClick={() => onPageChange(page - 1)}
              disabled={page <= 1}
            >
              ← Назад
            </button>
          </li>
          
          <li className={`page-item ${page >= totalPages ? 'disabled' : ''}`}>
            <button 
              className="page-link" 
              onClick={() => onPageChange(page + 1)}
              disabled={page >= totalPages}
            >
              Вперед →
            </button>
          </li>
        </ul>
      </nav>
    </div>
  );
}

export default Pagination;

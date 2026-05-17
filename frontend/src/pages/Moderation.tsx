import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../service/api';
import { ModeratedAlgorithm } from '../types';
import { ALGORITHM_STATUS_DISPLAY, ALGORITHM_STATUS_COLORS } from '../utils/constants';
import { hasModerationAccess, getUserRoleDisplay } from '../utils/authUtils';
import './Moderation.css';

const Moderation: React.FC = () => {
  const [algorithms, setAlgorithms] = useState<ModeratedAlgorithm[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedAlgorithm, setSelectedAlgorithm] = useState<ModeratedAlgorithm | null>(null);
  const [moderationDialogOpen, setModerationDialogOpen] = useState(false);
  const [rejectionReason, setRejectionReason] = useState('');
  const [actionLoading, setActionLoading] = useState(false);
  const [activeTab, setActiveTab] = useState(0);
  const [actionType, setActionType] = useState<'approve' | 'reject' | null>(null);
  
  const { user } = useAuth();

  useEffect(() => {
    fetchModerationAlgorithms();
  }, [activeTab]);

  const fetchModerationAlgorithms = async () => {
    try {
      setLoading(true);
      setError('');

      let algorithmsData: ModeratedAlgorithm[] = [];
      
      if (activeTab === 0) {
        // Алгоритмы на модерации
        algorithmsData = await apiService.getModerationAlgorithms();
      } else {
        // Все алгоритмы
        algorithmsData = await apiService.getAllAlgorithms();
      }
      
      setAlgorithms(algorithmsData);
    } catch (err: any) {
      console.error('Error fetching moderation algorithms:', err);
      
      if (err.response?.status === 403) {
        setError('У вас нет прав для доступа к модерации');
      } else if (err.response?.status === 404) {
        setError('Эндпоинт модерации не найден. Возможно, требуется настройка бэкенда.');
      } else if (err.message?.includes('Network error')) {
        setError('Ошибка сети. Проверьте подключение к серверу.');
      } else {
        setError('Не удалось загрузить алгоритмы для модерации');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleOpenApproveDialog = (algorithm: ModeratedAlgorithm) => {
    setSelectedAlgorithm(algorithm);
    setActionType('approve');
    setModerationDialogOpen(true);
  };

  const handleOpenRejectDialog = (algorithm: ModeratedAlgorithm) => {
    setSelectedAlgorithm(algorithm);
    setActionType('reject');
    setRejectionReason('');
    setModerationDialogOpen(true);
  };

  const handleCloseModerationDialog = () => {
    setModerationDialogOpen(false);
    setSelectedAlgorithm(null);
    setRejectionReason('');
    setActionType(null);
  };

  const moderateAlgorithm = async () => {
    if (!selectedAlgorithm || !actionType) return;

    setActionLoading(true);
    try {
      const status = actionType === 'approve' ? 'approved' : 'rejected';
      await apiService.moderateAlgorithm(selectedAlgorithm.id, {
        status,
        rejection_reason: actionType === 'reject' ? rejectionReason : ''
      });
      
      // Удаляем алгоритм из списка после модерации
      setAlgorithms(prev => prev.filter(alg => alg.id !== selectedAlgorithm.id));
      handleCloseModerationDialog();
      
      setError('');
    } catch (err) {
      console.error('Error moderating algorithm:', err);
      setError('Не удалось выполнить модерацию');
    } finally {
      setActionLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    return ALGORITHM_STATUS_COLORS[status as keyof typeof ALGORITHM_STATUS_COLORS] || '#6b7280';
  };

  const truncateText = (text: string, maxLength: number) => {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
  };


  // Проверяем права доступа
  if (!user) {
    return (
      <div className="moderation-page">
        <div className="error-container">
          <div className="error-icon">🔒</div>
          <div className="error-text">
            Для доступа к панели модерации необходимо авторизоваться.
          </div>
          <Link to="/login" className="primary-btn" style={{marginTop: '1rem'}}>
            Войти в систему
          </Link>
        </div>
      </div>
    );
  }

  if (!hasModerationAccess(user)) {
    return (
      <div className="moderation-page">
        <div className="error-container">
          <div className="error-icon">🚫</div>
          <div className="error-text">
            <h3>Доступ запрещен</h3>
            <p>У вас нет прав для доступа к этой странице. Только модераторы и администраторы могут просматривать эту страницу.</p>
            
            <div className="user-info-details">
              <p><strong>Информация о вашем аккаунте:</strong></p>
              <ul>
                <li>Имя пользователя: {user.username}</li>
                <li>Определенная роль: {getUserRoleDisplay(user)}</li>
                <li>ID: {user.id}</li>
                <li>Email: {user.email}</li>
              </ul>
            </div>
            
            <p className="contact-admin">
              Если вы считаете, что это ошибка, обратитесь к администратору для получения прав модератора.
            </p>
          </div>
        </div>
      </div>
    );
  }

  const pendingAlgorithms = algorithms.filter(alg => alg.status === 'pending');
  const displayAlgorithms = activeTab === 0 ? pendingAlgorithms : algorithms;

  return (
    <div className="moderation-page">
      <div className="moderation-header">
        <h1 className="moderation-title">Панель модерации</h1>
        <p className="moderation-subtitle">
          Здесь вы можете просматривать и модерировать алгоритмы, отправленные пользователями.
        </p>
        <div className="user-info">
          Вы вошли как: <strong>{user.username}</strong> (Роль: {getUserRoleDisplay(user)})
        </div>
      </div>

      {error && (
        <div className={`error-banner ${error.includes('У вас нет прав') ? 'error' : 'warning'}`}>
          <div className="error-banner-content">
            <span className="error-banner-icon">⚠️</span>
            <span className="error-banner-text">{error}</span>
            <button 
              className="error-banner-close"
              onClick={() => setError('')}
            >
              ×
            </button>
          </div>
        </div>
      )}

      <div className="moderation-tabs">
        <button 
          className={`tab-button ${activeTab === 0 ? 'active' : ''}`}
          onClick={() => setActiveTab(0)}
        >
          На модерации ({pendingAlgorithms.length})
        </button>
        <button 
          className={`tab-button ${activeTab === 1 ? 'active' : ''}`}
          onClick={() => setActiveTab(1)}
        >
          Все алгоритмы
        </button>
      </div>

      {loading ? (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <div className="loading-text">Загрузка...</div>
        </div>
      ) : activeTab === 0 && pendingAlgorithms.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📋</div>
          <h3 className="empty-title">Нет алгоритмов для модерации</h3>
          <p className="empty-description">
            Все алгоритмы прошли модерацию. Новые появления появятся здесь автоматически.
          </p>
        </div>
      ) : (
        <div className="algorithms-grid">
          {displayAlgorithms.map((algorithm) => (
            <AlgorithmCard 
              key={algorithm.id} 
              algorithm={algorithm} 
              onApprove={handleOpenApproveDialog}
              onReject={handleOpenRejectDialog}
            />
          ))}
        </div>
      )}

      {/* Диалог модерации */}
      {moderationDialogOpen && selectedAlgorithm && (
        <div className="modal-overlay">
          <div className="moderation-modal">
            <div className="modal-header">
              <h3 className="modal-title">
                {actionType === 'approve' ? 'Одобрение алгоритма' : 'Отклонение алгоритма'}
              </h3>
              <button className="modal-close" onClick={handleCloseModerationDialog}>×</button>
            </div>
            
            <div className="modal-content">
              <div className="algorithm-preview">
                <h4 className="algorithm-name">{selectedAlgorithm.title}</h4>
                <p className="algorithm-author">
                  Автор: {selectedAlgorithm.author_name}
                </p>
                <p className="algorithm-description">
                  {truncateText(selectedAlgorithm.description, 150)}
                </p>
              </div>

              {actionType === 'approve' ? (
                <div className="confirmation-message">
                  <div className="confirmation-icon">✅</div>
                  <p>Вы уверены, что хотите одобрить этот алгоритм?</p>
                  <p className="confirmation-note">
                    После одобрения алгоритм станет видимым для всех пользователей на главной странице.
                  </p>
                </div>
              ) : (
                <div className="rejection-reason-input">
                  <label htmlFor="rejectionReason" className="input-label">
                    Причина отклонения *
                  </label>
                  <textarea
                    id="rejectionReason"
                    className="reason-textarea"
                    placeholder="Укажите причину отклонения алгоритма..."
                    value={rejectionReason}
                    onChange={(e) => setRejectionReason(e.target.value)}
                    rows={4}
                  />
                  <p className="input-helper">
                    Обязательно для заполнения. Эта причина будет показана автору алгоритма.
                  </p>
                </div>
              )}
            </div>

            <div className="modal-actions">
              <button 
                className="modal-btn cancel-btn"
                onClick={handleCloseModerationDialog}
                disabled={actionLoading}
              >
                Отмена
              </button>
              <button
                className={`modal-btn ${actionType === 'approve' ? 'approve-modal-btn' : 'reject-modal-btn'}`}
                onClick={moderateAlgorithm}
                disabled={actionLoading || (actionType === 'reject' && !rejectionReason.trim())}
              >
                <span className="btn-icon">
                  {actionType === 'approve' ? '✓' : '✕'}
                </span>
                {actionType === 'approve' ? 'Да, одобрить' : 'Отклонить'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Новый компонент карточки алгоритма в стиле главной страницы
const AlgorithmCard: React.FC<{ 
  algorithm: ModeratedAlgorithm;
  onApprove: (algorithm: ModeratedAlgorithm) => void;
  onReject: (algorithm: ModeratedAlgorithm) => void;
}> = ({ algorithm, onApprove, onReject }) => {
  return (
    <div className={`algorithm-card ${algorithm.isPaid ? 'paid' : 'free'} moderation-view`}>
      <div className="card-header">
        <div className="card-title-section">
          <h3 className="card-title">
            <Link to={`/algorithm/${algorithm.id}`}>{algorithm.title}</Link>
          </h3>
          <div className="card-meta">
            <span className="card-date">
              {new Date(algorithm.createdAt).toLocaleDateString('ru-RU')}
            </span>
          </div>
        </div>
        <div className="card-badges">
          <span className="language-badge">{algorithm.language}</span>
          <span className={`type-badge ${algorithm.isPaid ? 'paid' : 'free'}`}>
            {algorithm.isPaid ? (algorithm.price ? `${algorithm.price} руб.` : 'Платный') : 'Бесплатный'}
          </span>
          <span 
            className="status-badge"
            style={{ 
              backgroundColor: ALGORITHM_STATUS_COLORS[algorithm.status as keyof typeof ALGORITHM_STATUS_COLORS] || '#6b7280'
            }}
          >
            {ALGORITHM_STATUS_DISPLAY[algorithm.status]}
          </span>
        </div>
      </div>
      
      <p className="card-description">{algorithm.description}</p>
      
      <div className="card-details">
        <div className="detail-item">
          <span className="detail-label">👤 Автор</span>
          <span className="detail-value">{algorithm.author_name}</span>
        </div>
        <div className="detail-item">
          <span className="detail-label">⚙️ Компилятор</span>
          <span className="detail-value">{algorithm.compiler}</span>
        </div>
        <div className="detail-item">
          <span className="detail-label">📏 Код</span>
          <span className="detail-value">{algorithm.code?.length || 0} символов</span>
        </div>
      </div>

      {algorithm.tags.length > 0 && (
        <div className="card-tags">
          {algorithm.tags.map(tag => (
            <span key={tag} className="tag">{tag}</span>
          ))}
        </div>
      )}

      {algorithm.status === 'rejected' && algorithm.rejection_reason && (
        <div className="rejection-notice">
          <strong>Причина отклонения:</strong>
          <p>{algorithm.rejection_reason}</p>
        </div>
      )}

      {algorithm.moderated_by && (
        <div className="moderation-info">
          <span className="moderated-by">
            Модератор: {algorithm.moderated_by}
            {algorithm.moderated_at && (
              <> • {new Date(algorithm.moderated_at).toLocaleDateString('ru-RU')}</>
            )}
          </span>
        </div>
      )}

      {algorithm.status === 'pending' && (
        <div className="card-actions moderation-actions">
          <button
            className="action-btn approve-btn"
            onClick={() => onApprove(algorithm)}
          >
            <span className="btn-icon">✓</span>
            Одобрить
          </button>
          <button
            className="action-btn reject-btn"
            onClick={() => onReject(algorithm)}
          >
            <span className="btn-icon">✕</span>
            Отклонить
          </button>
          <Link
            to={`/algorithm/${algorithm.id}`}
            className="action-btn details-btn"
            target="_blank"
          >
            <span className="btn-icon">👁️</span>
            Подробнее
          </Link>
        </div>
      )}
    </div>
  );
};

export default Moderation;
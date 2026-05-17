import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Link, useNavigate } from 'react-router-dom';
import { apiService } from '../service/api';
import SiteFooter from '../components/SiteFooter';
import './Auth.css';

const Login: React.FC = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const tokens = await apiService.login(formData);
      
      localStorage.setItem('accessToken', tokens.access);
      localStorage.setItem('refreshToken', tokens.refresh);
      
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const user = await apiService.getCurrentUser();
      
      login(user, tokens);
      
      navigate('/');
      
    } catch (error) {
      console.error('Login error:', error);
      
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      
      if ((error as any).response?.status === 401) {
        setError('Неверное имя пользователя или пароль');
      } else if ((error as any).message) {
        setError((error as Error).message);
      } else {
        setError('Произошла неизвестная ошибка');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="auth-container">
        <div className="auth-form">
          <h2>Вход в систему</h2>
          {error && <div className="error-message">{error}</div>}
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="username">Имя пользователя</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
                disabled={loading}
              />
            </div>
            <div className="form-group">
              <label htmlFor="password">Пароль</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                disabled={loading}
              />
            </div>
            <button type="submit" disabled={loading} className="auth-button">
              {loading ? 'Вход...' : 'Войти'}
            </button>
          </form>
          <p className="auth-link">
            Нет аккаунта? <Link to="/register">Зарегистрируйтесь</Link>
          </p>
        </div>
      </div>
      <SiteFooter />
    </div>
  );
};

export default Login;
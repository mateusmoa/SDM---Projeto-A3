// Funções comuns para todas as interfaces
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se o usuário está logado
    const token = localStorage.getItem('token');
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    
    // Redirecionar para login se não estiver logado
    if (!token || !currentUser) {
        if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
            window.location.href = '/login';
        }
    } else {
        // Atualizar informações do usuário no cabeçalho
        const userNameElement = document.getElementById('userName');
        const userTypeElement = document.getElementById('userType');
        
        if (userNameElement) {
            userNameElement.textContent = currentUser.nome;
        }
        
        if (userTypeElement) {
            userTypeElement.textContent = currentUser.tipo.charAt(0).toUpperCase() + currentUser.tipo.slice(1);
        }
    }
    
    // Configurar botão de logout
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            localStorage.removeItem('token');
            localStorage.removeItem('currentUser');
            window.location.href = '/login';
        });
    }
});

// Função para fazer requisições à API
async function apiRequest(endpoint, method = 'GET', data = null) {
    const token = localStorage.getItem('token');
    
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    };
    
    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`/api${endpoint}`, options);
        const responseData = await response.json();
        
        if (!response.ok) {
            throw new Error(responseData.message || 'Ocorreu um erro na requisição');
        }
        
        return responseData;
    } catch (error) {
        showAlert(error.message, 'danger');
        console.error('Erro na requisição:', error);
        throw error;
    }
}

// Função para mostrar alertas
function showAlert(message, type = 'info') {
    const alertsContainer = document.getElementById('alerts');
    if (!alertsContainer) return;
    
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${type} fade-in`;
    alertElement.textContent = message;
    
    alertsContainer.appendChild(alertElement);
    
    // Remover alerta após 5 segundos
    setTimeout(() => {
        alertElement.style.opacity = '0';
        setTimeout(() => {
            alertsContainer.removeChild(alertElement);
        }, 300);
    }, 5000);
}

// Função para formatar data
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR') + ' ' + date.toLocaleTimeString('pt-BR', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Função para mostrar/esconder loader
function toggleLoader(show = true) {
    const loader = document.getElementById('loader');
    if (!loader) return;
    
    loader.style.display = show ? 'block' : 'none';
}

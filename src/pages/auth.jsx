export const AuthPage = () => {
    return (
        <main className='main-auth'>
            <header className='main__header'>
                <img src="./image/logo.png" alt="Digital Queue"  className='main__header-logo'/>
                <div className="main__header-wrapper">
                <h2 className='main__header-title'>Name of project</h2>
                </div>
            </header>

            <div className="auth__block" >
                <div className="auth-wrap">
                    <img src="./image/admin.png" alt="admin" className='auth-img'/>
                    <span className='textAuth-admin'>Организатор</span>
                </div>

                <form action="#" method="post" className="auth__form">
                    <input type="text" className="auth__login input__optional" placeholder="Логин"/>
                    <input type="password" className="auth__password input__optional" placeholder="Пароль"/>
                    <a href="/admin" className="auth__button">войти</a>
                </form>
            </div>

            <div className="empty-block"></div>
        </main>
    )
}
export const MainPage = () => {
    return (
    <main className='main'>
      <div className='container'>
        <header className='main__header'>
            <img src="./image/logo.png" alt="Digital Queue"  className='main__header-logo'/>
            <div className="main__header-wrapper">
            <h2 className='main__header-title'>Name of project</h2>
            </div>
        </header>
    
        <div className="main__change-block">
            <div className="main__change-block-user change-block__property">
                <div className="change-block-user__select select-option">
                    <img src="./image/user.png" alt="user" className='option-img'/>
                    <p className='text-user'>Участник</p>
                </div>
            </div>

            <div className='main_change-block-lineOr'>
                <img src="./image/line.png" alt="error" className='line-img'/>
                <span>или</span>
                <img src="./image/line.png" alt="error" className='line-img'/>
            </div>

            <div className="main__change-block-admin change-block__property" >
                <a href="/auth" className="authLink">
                    <div className="change-block-user__select select-option" >
                        <img src="./image/admin.png" alt="admin" className='option-img'/>
                        <p className='text-admin'>Организатор</p>
                    </div>
                </a>
            </div>
          </div>
        </div>
    </main>);
}
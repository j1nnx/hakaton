export const AdminPage = () => {
    let time = 10;
    let PcCount = 10;
    let ProjectName = document.getElementsByClassName('main__header-title-admin').value
    let login = 'Ivan1998';
    let count = [
        {name: 'Ivan', surname: 'Ivanov',id: '@User'}, 
        {name: 'Ivan', surname: 'Ivanov',id: '@User'}, 
        {name: 'Ivan', surname: 'Ivanov',id: '@User'},
        {name: 'Ivan', surname: 'Ivanov',id: '@User'},
        {name: 'Ivan', surname: 'Ivanov',id: '@User'},
        {name: 'Ivan', surname: 'Ivanov',id: '@User'},
        {name: 'Ivan', surname: 'Ivanov',id: '@User'},
        {name: 'Ivan', surname: 'Ivanov',id: '@User'}
    ];


    return (
        <main className='main-admin'>
            <header className='main__header'>
                <img src="./image/logo.png" alt="Digital Queue"  className='main__header-logo'/>
                <div className="main__header-wrapper">
                <input type='text' className='main__header-title-admin before__disable'/>
                </div>
            </header>

        <div className="main__AdminWrapper">
            <div className="main__admin-settings">
                <p className="setting-text fz-long before1">Время на 1 человека: {time} мин.</p>
                <p className="setting-text before2">Кол-во стендов/ПК: {PcCount} шт.</p>
            </div>


            <div className="main__table">
                <span className="member-list-text">Список участников</span>

                <div className="UlListWrapper">
                    <ul className="main__table-list">
                        <div className="table-list__legend">     
                            <div className="legend-option"><span>Имя</span></div>
                            <div className="legend-option flex-end"><span>номер</span></div>
                            <div className="legend-option flex-end"><span>@id</span></div>
                            <div className="legend-option"><span>-</span></div>
                        </div>
                        {count.map((e, idx) => (
                            <li className="table-li" key={idx}>
                                <div className={`${idx % 2 === 0 ? 'green-black position' : 'green-white position'}`}>
                                    <span className="UserNames">{e.name} {e.surname}</span> 
                                    <span className="UserPlaceCount">{idx + 1}</span>
                                    <span className="UserTgId">{e.id}</span>
                                    <button>D</button>
                                    </div>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>

            <div className="main__UserPanel-name">
                <img src="./image/admin.png" alt="admin" className='admin-img'/>
                <span className="AdminName-text">Организатор {login}</span> 
            </div>
        </div>

        </main>
    )
}
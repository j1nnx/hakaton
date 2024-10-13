export const AdminPage = () => {
    let time = 10;
    let PcCount = 10;
    let ProjectName = document.getElementsByClassName('main__header-title-admin').value
    let login = 'Ivan1998';
    let count = [
        {name: 'Ivan', surname: 'Ivanov',id: '52'}, 
        {name: 'Ivan', surname: 'Ivanov',id: '52'}, 
        {name: 'Ivan', surname: 'Ivanov',id: '52'},
        {name: 'Ivan', surname: 'Ivanov',id: '52'},
        {name: 'Ivan', surname: 'Ivanov',id: '52'},
        {name: 'Ivan', surname: 'Ivanov',id: '52'},
        {name: 'Ivan', surname: 'Ivanov',id: '52'},
        {name: 'Ivan', surname: 'Ivanov',id: '52'}
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
                <p className="setting-text fz-long">Время на 1 человека: <input type='number' className='info-input' defaultValue={time} /> мин.</p>
                <p className="setting-text">Кол-во стендов/ПК: <input type='number' className='info-input' defaultValue={PcCount}/> шт.</p>
            </div>


            <div className="main__table">
                <span className="member-list-text">Список участников</span>

                <div className="UlListWrapper">
                    <ul className="main__table-list">
                        <div className="table-list__legend">     
                            <div className="legend-option "><span>-</span></div>
                            <div className="legend-option "><span>Имя</span></div>
                            <div className="legend-option "><span>№</span></div>
                            <div className="legend-option"><span>-</span></div>
                        </div>
                        {count.map((e, idx) => (
                            <li className="table-li" key={idx}>
                                <div className={`${idx % 2 === 0 ? 'green-white position' : 'green-black position'}`}>
                                   <div className="legend-wrapper"> <span className="UserPlaceCount">#{idx + 1}</span> </div>

                                    <div className="legend-wrapper"><span className="UserNames">{e.name} {e.surname}</span> </div>

                                    <div className="legend-wrapper"><span className="UserTgId">{e.id}</span></div>

                                    <div className="legend-wrapper"><button>D</button></div>
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
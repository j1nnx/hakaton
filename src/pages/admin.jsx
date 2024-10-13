import { useState, useEffect } from "react";

export const AdminPage = () => {
    let [time, setTime] = useState(1); // Стейт для времени на одного человека
    let [title, setTitle] = useState(""); // Стейт для заголовка
    let [pcCount, setPcCount] = useState(1); // Стейт для количества ПК/терминалов
    let [users, setUsers] = useState([]); // Стейт для списка участников
    let login = 'Ivan1998';  // Пример логина

    // URL вашего FastAPI сервера
    const API_URL = "http://localhost:8000";

    // useEffect для получения заголовка
    useEffect(() => {
        fetch(`${API_URL}/title`)
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Network response was not ok.');
                }
            })
            .then(data => {
                setTitle(data.title);  // Устанавливаем заголовок
                console.log("Current title:", data.title);
            })
            .catch(error => {
                console.error("There was a problem with the fetch operation:", error);
            });
    }, []);

    // useEffect для получения времени на одного человека
    useEffect(() => {
        fetch(`${API_URL}/time/`)
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Network response was not ok.');
                }
            })
            .then(data => {
                setTime(data.time);  // Устанавливаем время на одного человека
                console.log("Time per person:", data.time);
            })
            .catch(error => {
                console.error("There was a problem with the fetch operation:", error);
            });
    }, []);

    // useEffect для получения количества ПК/терминалов
    useEffect(() => {
        fetch(`${API_URL}/attractions/`)
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Network response was not ok.');
                }
            })
            .then(data => {
                setPcCount(data.number_attractions);  // Устанавливаем количество ПК/терминалов
                console.log("Number of terminals:", data.number_attractions);
            })
            .catch(error => {
                console.error("There was a problem with the fetch operation:", error);
            });
    }, []);

    // useEffect для получения списка участников
    useEffect(() => {
        fetch(`${API_URL}/all_queue/`)
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Network response was not ok.');
                }
            })
            .then(data => {
                setUsers(data.queue || []);  // Устанавливаем список участников
                console.log("Users in queue:", data.queue);
            })
            .catch(error => {
                console.error("There was a problem with the fetch operation:", error);
            });
    }, []);

    // Функция для обновления времени на человека
    const handleTimeChange = (event) => {
        const newTime = event.target.value;
        setTime(newTime);

        // Отправляем POST запрос на сервер для обновления времени через query параметры
        fetch(`${API_URL}/time/?new_time=${newTime}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log("Time updated:", data.message);
        })
        .catch(error => {
            console.error("There was an error updating time:", error);
        });
    };

    // Функция для обновления количества ПК/терминалов
    const handlePcCountChange = (event) => {
        const newPcCount = event.target.value;
        setPcCount(newPcCount);

        // Отправляем POST запрос на сервер для обновления количества ПК/терминалов через query параметры
        fetch(`${API_URL}/attractions/?attractions=${newPcCount}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log("PC count updated:", data.message);
        })
        .catch(error => {
            console.error("There was an error updating PC count:", error);
        });
    };

    // Функция для обновления названия
    const handleTitleChange = (event) => {
        const newTitle = event.target.value;
        setTitle(newTitle);

        // Отправляем POST запрос на сервер для обновления названия через query параметры
        fetch(`${API_URL}/title/?new_title=${newTitle}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log("Title updated:", data.message);
        })
        .catch(error => {
            console.error("There was an error updating title:", error);
        });
    };

    // Функция для удаления пользователя
    const handleRemoveUser = (userId) => {
        // Отправляем DELETE запрос на сервер для удаления пользователя из очереди
        fetch(`${API_URL}/remove_from_queue/${userId}`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to remove user');
            }
        })
        .then(data => {
            console.log(data.message);
            // Перезагружаем страницу после успешного удаления пользователя
            window.location.href = window.location.href;
        })
        .catch(error => {
            console.error("There was an error removing the user:", error);
            window.location.href = window.location.href;
        });
    };

    return (
        <main className='main-admin'>
            <header className='main__header'>
                <img src="../image/logo.png" alt="Digital Queue" className='main__header-logo' />
                <div className="main__header-wrapper">
                    {/* Обработчик изменения заголовка */}
                    <input
                        type='text'
                        className='main__header-title-admin before__disable'
                        value={title}
                        onChange={handleTitleChange}  // Обработчик изменения заголовка
                    />
                </div>
            </header>

            <div className="main__AdminWrapper">
                <div className="main__admin-settings">
                    <p className="setting-text fz-long">
                        Время на 1 человека:
                        <input
                            type='number'
                            className='info-input'
                            value={time}
                            onChange={handleTimeChange}  // Обработчик изменения времени
                        /> мин.
                    </p>
                    <p className="setting-text">
                        Кол-во стендов/ПК:
                        <input
                            type='number'
                            className='info-input'
                            value={pcCount}
                            onChange={handlePcCountChange}  // Обработчик изменения количества ПК
                        /> шт.
                    </p>
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
                            {users.map((e, idx) => (
                                <li className="table-li" key={idx}>
                                    <div className={`${idx % 2 === 0 ? 'green-white position' : 'green-black position'}`}>
                                        <div className="legend-wrapper"><span className="UserPlaceCount">#{e.position}</span></div>
                                        <div className="legend-wrapper"><span className="UserNames">{e.username}</span></div>
                                        <div className="legend-wrapper"><span className="UserTgId">{e.user_id}</span></div>
                                        <div className="legend-wrapper">
                                            <button className="delete_user" onClick={() => handleRemoveUser(e.user_id)}>
                                                Удалить
                                            </button>
                                        </div>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>

                <div className="main__UserPanel-name">
                    <img src="./image/admin.png" alt="admin" className='admin-img' />
                    <span className="AdminName-text">Организатор {login}</span>
                </div>
            </div>
        </main>
    );
};

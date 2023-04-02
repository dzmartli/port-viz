import LogoSVG from './assets/logo.svg';

function Logo() {
    return (
        <>
            <div className='logo'>
                <img src={LogoSVG} alt="Logo svg" />
            </div>
        </>
    );
}

export default Logo;
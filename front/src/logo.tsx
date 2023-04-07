import LogoSVG from './assets/logo.svg';
import { memo } from 'react';

function Logo() {
    return (
        <>
            <div className='logo'>
                <img src={LogoSVG} alt="Logo svg" />
            </div>
        </>
    );
}

export default memo(Logo);
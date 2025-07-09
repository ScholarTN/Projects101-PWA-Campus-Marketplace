import styles from './welcome_banner.module.css';

import bannerImageSource from '../assets/logo.jpeg';
function WelcomeBanner({
  imageUrl = bannerImageSource,
  altText = "Welcome banner graphic",
  greeting = "Hello user. What shall we do for you today?",
  header = ""
}) {


  return (
    <div className={styles.container}>
      <h1 className={styles.header} >
        {header}  
      </h1>
      <img
        src={imageUrl}
        alt={altText}
        className={styles.bannerImage}
      />
      <p className={styles.greetingText}>
        {greeting}
      </p>
    </div>
  );
}

export default WelcomeBanner;
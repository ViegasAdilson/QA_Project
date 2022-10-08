

CREATE SCHEMA IF NOT EXISTS `agenda` DEFAULT CHARACTER SET utf8 ;
USE `agenda` ;


CREATE TABLE IF NOT EXISTS `agenda`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(30) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  `passwd` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `agenda`.`contacts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `surname` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(15) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `address` VARCHAR(45) NOT NULL,
  `description` VARCHAR(1024) NOT NULL,
  `picture` VARCHAR(30) NOT NULL,
  `id_user` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk1_contacto_1_idx` (`id_user` ASC) VISIBLE,
  CONSTRAINT `fk1_contacto_1`
    FOREIGN KEY (`id_user`)
    REFERENCES `agenda`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

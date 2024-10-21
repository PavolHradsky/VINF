from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


def tokenize(line: str) -> list[str]:
    line = line.lower()
    line = line.replace("\t", " ")
    line = line.replace(",", " ")
    line = line.replace(".", " ")
    line = line.replace("/", " ")
    line = line.replace(";", " ")
    line = line.replace("\"", " ")
    line = line.replace("\'", " ")
    line = line.replace("(", " ")
    line = line.replace(")", " ")
    line = line.replace("[", " ")
    line = line.replace("]", " ")
    line = line.replace("*", " ")
    line = line.replace(":", " ")
    line = line.replace("!", " ")
    line = line.replace("+", " ")
    line = line.replace("=", " ")
    words = line.split()
    return words


def create_driver(version: int = 129):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ")
    return uc.Chrome(options=options, version_main=version)
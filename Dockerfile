FROM python
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install requests.auth
RUN pip install bs4
RUN pip install pandas
RUN pip install pywebio
RUN pip install lxml
ADD nagios.py /home/nagios.py
CMD ["/home/nagios.py"]
ENTRYPOINT ["python"]

class Document:
	def __init__(self, pid, name, power, kp, deaths, t4_kills, t5_kills):
		self._pid = pid
		self._name = name
		self._power = power
		self._kp = kp
		self._deaths = deaths
		self._t4_kills = t4_kills
		self._t5_kills = t5_kills

	@staticmethod
	def newInstance():
		return Document(0, '', 0, 0, 0, 0, 0)

	# Getters and Setters
	@property
	def pid(self):
		return self._pid

	@pid.setter
	def pid(self, pid):
		self._pid = pid

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, name):
		self._name = name

	@property
	def power(self):
		return self._power

	@power.setter
	def setter(self, power):
		self._power = power

	@property
	def kp(self):
		return self._kp

	@kp.setter
	def kp(self, kp):
		self._kp = kp

	@property
	def deaths(self):
		return self._deaths
	
	@deaths.setter
	def deaths(self, deaths):
		self._deaths = deaths

	@property
	def t4_kills(self):
		return self.__t4_kills

	@t4_kills.setter
	def t4_kills(self, t4_kills):
		self._t4_kills = t4_kills

	@property
	def t5_kills(self):
		return self._t5_kills

	@t5_kills.setter
	def t5_kills(self, t5_kills):
		self._t5_kills = t5_kills

	def __str__(self):
		return (
			f"Player ID: {self._pid}\n"
			f"Name: {self._name}\n"
			f"Power: {self._power}\n"
			f"Kill Points: {self._kp}\n"
			f"Deaths: {self._deaths}\n"
			f"T4 Kills: {self._t4_kills}\n"
			f"T5 Kills: {self._t5_kills}"
		)

import random,time
from card import Card
from user import User

class Atm:
	def __init__(self,allUserInfo):
		self.allUserInfo = allUserInfo

	#检测密码	
	def isExistPwd(self,inputCard):
		if self.allUserInfo.get(inputCard).cardInfo.status:
			 print("此卡已锁定，没有必要输入密码，请联系管理员!")
			 return False
		for i in range(3):
			inputPwd = input("请输入密码:")
			if inputPwd == self.allUserInfo.get(inputCard).cardInfo.cardPwd:
				return True	
			else:
				print("密码输入错误，还有%s次输入机会"%(2-i))

		else:
			self.allUserInfo.get(inputCard).cardInfo.status = True  #锁定卡
			print("此卡已锁定！")
			return False		
		
			
	#判断卡号是否存在	
	def isExistCard(self,cardNum):
		if not self.allUserInfo.get(cardNum):
			print("暂无此卡")
			return False
		return True	
	
	#随机生成卡号	
	def randomCardNum(self):
		#print
		cardnum = ''
		#卡号一共6位
		for i in range(6):
			cardnum += str(random.randint(0,9))

		#判断生成卡号有没有重复	
		#{1212:user1,2323:user2,1213:user3}
		# for i in self.allUserInfo:   #字典遍历  下标（键）{'name':'zs'}  {cardnum:用户对象}
		# 
		# 
		# 	if i == cardnum:
		# 		self.randomCardNum()

		#通过get方法查找  生成的卡号是否有存在，若存在则重新生成（函数自调用）
		if self.allUserInfo.get(cardnum):
			self.randomCardNum()		
		
		return cardnum	

		
			
	#检测确认密码	
	def checkPwd(self,onePwd):
		#
		for i in range(3):

			two = input("请再次输入确认密码:")
			if two == onePwd:
				print("确认密码一致")
				return True	
			else:
				print("密码输入错误，还有%s次输入机会"%(2-i))

		else:
			print("确认密码三次用完")
			return False		

	#开卡
	def createUser(self):
		name = input('请输入姓名：')
		idCard = input('请输入身份证号：')
		phone = input('请输入电话号：')
		money = input('请输入预存金额：')

		#预存金额是否大于1
		if int(money) < 1:
			print("预存金额不足，开卡失败！")
			return False

		onePwd = input("请输入卡密码：")

		twoPwd = self.checkPwd(onePwd)  #调用检查确认密码	
		#确认密码三次机会用完
		if not twoPwd:
			print("开卡失败！")
			return False

		#以上没有问题，进行开卡
		
		#随机生成卡号  
		cardNum = self.randomCardNum()

		#创建卡对象
		card = Card(cardNum,onePwd,money)
		#用户对象
		self.allUserInfo[cardNum]=User(name,idCard,phone,card)

		# aa = {'name':'zs'}
		# aa['name']='12212' 

		time.sleep(1)
		print("开卡成功!请牢记您的卡号%s"%cardNum)
		return 	
			


	#解卡
	   #。。。。。status = False 
	def unstatus(self):
		while True:
			unstatusCard = input("请输入锁定的卡号：")
			if not self.isExistCard(unstatusCard):
				self.unstatus()

			if self.allUserInfo.get(unstatusCard).cardInfo.status == False:
				print("%s此卡没有被锁定，无需解卡！"%(unstatusCard))
				return False
			self.allUserInfo.get(unstatusCard).cardInfo.status = False
			return True
	#查询
		#当前登录用户卡号， self.allUserInfo.get(inputCard).cardInfo.mone
	def findMoney(self,inputCard):
		print("您当前卡内余额为%s"%(self.allUserInfo.get(inputCard).cardInfo.money))
	#存款
		#当前登录用户卡号  输入存款  0>(附加 0~2500)  余额+存入金额
	def inMoney(self,inputCard):
		inMoney = input("请输入存款金额：")
		self.allUserInfo.get(inputCard).cardInfo.money = str(int(self.allUserInfo.get(inputCard).cardInfo.money) + int(inMoney))
		print("存款成功！当前卡内余额还剩%s"%(self.allUserInfo.get(inputCard).cardInfo.money))
	#取款     
		#当前登录用户卡号  输入取款 
	def outMoney(self,inputCard):		
		oldMoney = int(self.allUserInfo.get(inputCard).cardInfo.money)
		if oldMoney == 0:
			print("您的卡里没有金额，无法进行取款！")
			return False
		while True:
			outmoney = input("请输入取款金额：")
			if int(outmoney) <= 0:
				print("输入错误，请重新输入")
				continue

			if int(outmoney) > oldMoney:
				print("余额不足！")
				continue
			self.allUserInfo.get(inputCard).cardInfo.money = str(int(oldMoney)-int(outmoney))
			print("当前还剩余额%s"%(self.allUserInfo.get(inputCard).cardInfo.money))
			return True

	#转账   
	def transMoney(self,inputCard):
		transCard = input("请输入要转账的卡号：")
		#没有此卡
		if not self.isExistCard(transCard):
			self.transMoney(inputCard)


		if 	transCard == inputCard:
			print("不能给自己转账！")
			return	
		if self.allUserInfo.get(transCard).cardInfo.status:
			print("对方账号被锁定，无法转账！")
			return
		transmoney = input("请输入转账金额：")			
		if  int(transmoney) <= 0:
			print("输入错误，请重新输入")
			return

		if int(self.allUserInfo.get(inputCard).cardInfo.money) > int(transmoney):
			self.allUserInfo.get(inputCard).cardInfo.money =str(int(self.allUserInfo.get(inputCard).cardInfo.money)-int(transmoney))
			self.allUserInfo.get(transCard).cardInfo.money =str(int(self.allUserInfo.get(transCard).cardInfo.money)+int(transmoney))
			print("转账成功！当前卡余额还剩%s"%(self.allUserInfo.get(inputCard).cardInfo.money))
			return
		else:
	 		print("卡内余额不足，请重新操作！")

	#修改密码	
	#确认密码3次   没有修改成功
	def updatePwd(self,inputCard):
		newPwd = input("请输入新的密码：")
		if self.checkPwd(newPwd):
			self.allUserInfo.get(inputCard).cardInfo.cardPwd = newPwd
			return True
		return False

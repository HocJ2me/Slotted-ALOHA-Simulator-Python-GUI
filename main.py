import tkinter
import tkinter.messagebox
import customtkinter


from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import io
from PIL import Image
import PIL

from tkinter import *
import numpy as np


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("MÔ PHỎNG HOẠT ĐỘNG VÀ ĐÁNH GIÁ HIỆU QUẢ CỦA KÊNH TRUYỀN")
        self.geometry(f"{1100}x{700}")

        # configure grid layout (2x10)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=0)
        self.grid_rowconfigure(( 3 ,4, 5,6,7,8,9, 10), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label1 = customtkinter.CTkLabel(self.sidebar_frame, text="MÔ HÌNH MẠNG SLOTTED ALOHA", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.logo_label1 = customtkinter.CTkLabel(self.sidebar_frame, text="GVHD: PGS. TS. Trần Quang Vinh ",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label1.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.logo_label2 = customtkinter.CTkLabel(self.sidebar_frame, text="SVTH: Nhóm 11 (142104 - ET4291)",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label2.grid(row=2, column=0, padx=20, pady=(20, 10))

        
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.infinite_slotted_aloha)
        self.sidebar_button_1.grid(row=7, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.finite_slotted_aloha)
        self.sidebar_button_2.grid(row=9, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.exit_button_event)
        self.sidebar_button_3.grid(row=10, column=0, padx=20, pady=10)



        ports = ['5','8','10','25','50','70','100','200']
        self.T_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=['1000000', '500000', '250000', '100000', '10000', '1000'],
                                                               command=self.change_T_event)
        self.T_optionemenu.grid(row=5, column=0,  padx=20, pady=(20, 10)) 
        
        self.load_scale_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=['0.1', '0.5', '1', '5', '10', '50'],
                                                               command=self.change_load_scale_event)
        self.load_scale_optionemenu.grid(row=6, column=0,  padx=20, pady=(20, 10))


               

        self.num_STAs_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=ports,
                                                                       command=self.change_port_name_event)
        self.num_STAs_optionemenu.grid(row=8, column=0,  padx=20, pady=(20, 10))
        
##        self.packet_rate_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=['0.2', '8'],
##                                                               command=self.change_baud_rate_event)
##        self.packet_rate_optionemenu.grid(row=8, column=0,  padx=20, pady=(20, 10))
##

        # set default values
        self.load_scale = 0.1
        self.T = 1000000
        self.number_STA = 10
        
        self.sidebar_button_1.configure(text="Trường hợp trạm vô hạn")
        self.sidebar_button_2.configure(text="Trường hợp trạm hữu hạn")
        self.sidebar_button_3.configure(text="Exit")
        self.num_STAs_optionemenu.set("Số trạm")
##        self.packet_rate_optionemenu.set('Tốc độ truyền')
        self.T_optionemenu.set("T - # access cycles")
        self.load_scale_optionemenu.set("Load scale")

        self.port_name = ""
        self.baud_rate = 0

        self.label_throughput_fig = customtkinter.CTkLabel(self, text="THÔNG LƯỢNG TRUNG BÌNH")
        self.label_throughput_fig.grid(column=1, row=0)

        self.label_collision_fig = customtkinter.CTkLabel(self, text="Xác suất va trạm")
        self.label_collision_fig.grid(column=1, row=1)
        
        self.label_debug = customtkinter.CTkLabel(self, text="")
        self.label_debug.grid(column=1, row=3)


    def change_load_scale_event(self, new_scale: str):
         self.load_scale = float(new_scale)
         
    def change_T_event(self, new_T: str):
         self.T = int(new_T)
        
    def change_port_name_event(self, new_port_name: str):
        self.number_STA = int(new_port_name)

    def change_baud_rate_event(self, new_baud_rate: str):
        self.baud_rate = new_baud_rate

    def infinite_slotted_aloha(self):
        T = self.T 
        load_scale = self.load_scale

        text_debug = "infinite(T=" + str(T) + ",load_scale=" + str(load_scale) + ")"
        self.label_debug.configure(text=text_debug)
        app.update()
        
        G = np.arange(0,18+load_scale,load_scale)
        request = np.zeros((T + 1,len(G)+1))

        print((request[1][:].shape))

        slotted_ALOHA_success = np.zeros((1,len(G)))[0]
        slotted_ALOHA_collision = np.zeros((1,len(G)))[0]

        for g in np.arange(1,len(G)).reshape(-1):
            request[:,g] = np.random.poisson(G[g],T + 1)

        for g in np.arange(1,len(G)+1).reshape(-1):
            for t in np.arange(1,T+1).reshape(-1):
                if request[t,g] == 1:
                    slotted_ALOHA_success[g] = slotted_ALOHA_success[g] + 1
                if request[t,g] > 1:
                    slotted_ALOHA_collision[g] = slotted_ALOHA_collision[g] + 1

        ## calculate
        # slotted ALOHA
        S_slotted_ALOHA = slotted_ALOHA_success / T
        collision_prob = slotted_ALOHA_collision / T
        print(S_slotted_ALOHA)
        print(collision_prob)

        ## plot
        # slotted
       
        
        plt.figure(1).clear()
        plt.plot(G,S_slotted_ALOHA,'-x', label="simulation " + text_debug)
        plt.title('Average Throughput of Slotted ALOHA')
        plt.xlabel('G')
        plt.ylabel('Average Throughput')
        S = np.multiply(G,np.exp(- G))
        plt.plot(G,S,label='analytical ' + text_debug)
        plt.legend()
        plt.savefig('foo.png')
        im = PIL.Image.open('foo.png')
        button_image = customtkinter.CTkImage(im, size=(480, 320))
        self.label_throughput_fig.configure(image=button_image, text= "")
        
        plt.figure(2).clear()
        plt.plot(G,collision_prob,'-s',label="simulation " + text_debug)
        plt.title('Collision Probability of Slotted ALOHA')
        plt.xlabel('G')
        plt.ylabel('Collision Probability')
        collision_prob_ana = 1 - np.exp(- G) - np.multiply(G,np.exp(- G))
        plt.plot(G,collision_prob_ana,label='analytical ' + text_debug)
        plt.legend()
        plt.savefig('too.png')

        im = PIL.Image.open('too.png')
        button_image = customtkinter.CTkImage(im, size=(480, 320))
        self.label_collision_fig.configure(image=button_image, text= "")
        

    def finite_slotted_aloha(self, ):
        import numpy as np
        import matplotlib.pyplot as plt
        i = 1

        trafficOffered = np.full((50, 50),0).tolist()
        throughput = np.full((50, 50),0).tolist()
        pcktCollisionProb = np.full((50, 50),0).tolist()

        for sourceNumber in np.array([self.number_STA]).reshape(-1):
            j = 1
            for lambda_ in np.array([np.arange(0,8+0.2,0.2)]).reshape(-1):
                simulationTime = self.T
                sourceStatus = np.zeros((1,sourceNumber+1))[0]
                # 0: idle source
        # 1: active
                attemptSource = 0
                pcktTransmissionAttempts = 0
                #nodeDelay = zeros(1, sourceNumber);
        #sumDelay=0;
                ackdPacketCount = 0
                pcktCollisionCount = 0
                currentSlot = 0
                pr = lambda_ / sourceNumber
                #fileID = fopen('lambda5.txt','w');
                while currentSlot < simulationTime:

                    currentSlot = currentSlot + 1
                    #fprintf(fileID, 'slot = #i \n', currentSlot);
                    transmissionAttemptsEachSlot = 0
                    for source in np.arange(1,sourceNumber+1).reshape(-1):
                        if sourceStatus[source] == 0 and np.random.rand(1) <= pr:
                            sourceStatus[source] = 1
                            #nodeDelay(source)=0;
                            transmissionAttemptsEachSlot = transmissionAttemptsEachSlot + 1
                            pcktTransmissionAttempts = pcktTransmissionAttempts + 1
                            attemptSource = source
                            #fprintf(fileID, 'station #d is transmitting new packet \n', source);
                        else:
                            if sourceStatus[source] == 1:
                                #nodeDelay(source) = nodeDelay(source)+1;
                                if np.random.rand(1) <= pr:
                                    transmissionAttemptsEachSlot = transmissionAttemptsEachSlot + 1
                                    pcktTransmissionAttempts = pcktTransmissionAttempts + 1
                                    attemptSource = source
                                    #fprintf(fileID, 'station #d is transmitting backlogged packet \n', source);
                    if transmissionAttemptsEachSlot == 1:
                        ackdPacketCount = ackdPacketCount + 1
                        #sumDelay = sumDelay+nodeDelay(attemptSource);
                        sourceStatus[attemptSource] = 0
                        #fprintf(fileID, 'station #d packet is successfull with delay #d \n', attemptSource, nodeDelay(attemptSource));
                    else:
                        if transmissionAttemptsEachSlot > 1:
                            pcktCollisionCount = pcktCollisionCount + 1
                            #fprintf(fileID, 'COLLISION Happens \n');
                print(i,j)
                trafficOffered[i][j] = pcktTransmissionAttempts / currentSlot
                #     if ackdPacketCount == 0
        #         meanDelay = simulationTime; # theoretically, if packets collide continously, the delay tends to infinity
        #     else
        #         meanDelay = sumDelay/ackdPacketCount;
        #     end
                throughput[i][j] = ackdPacketCount / currentSlot
                pcktCollisionProb[i][j] = pcktCollisionCount / currentSlot
                #fileID.close();
                j = j + 1
            i = i + 1

        ## plot
        plt.figure(1)
        plt.plot(trafficOffered[1][:],throughput[1][:],'-x', label="simulation, M="+str(self.number_STA))
        plt.title('Average Throughput of Finite-Station Slotted ALOHA')
        plt.xlabel('G (Offered Traffic)')
        plt.ylabel('Average Throughput')
        G = np.array([np.arange(0,8+0.2,0.2)])
        S = np.multiply(G,(1 - G / 10) ** (10 - 1))
        ##plt.plot(G,S)
##        plt.plot(trafficOffered[2][:],throughput[2][:],'-s', label="simulation, M=25")
##        S = np.multiply(G,(1 - G / 25) ** (25 - 1))
        ##plt.plot(G,S)
##        plt.plot(trafficOffered[3][:],throughput[3][:],'-o', label="simulation, M=50")
##        S = np.multiply(G,(1 - G / 50) ** (50 - 1))
        ##plt.plot(G,S)
        #plt.legend('simulation, M=10','analytical, M=10','simulation, M=25','analytical, M=25','simulation, M=50','analytical, M=50')
        plt.legend()
        plt.savefig('foo.png')
        im = PIL.Image.open('foo.png')
        button_image = customtkinter.CTkImage(im, size=(480, 320))
        self.label_throughput_fig.configure(image=button_image, text= "")

        plt.figure(2)
        plt.plot(trafficOffered[1][:],pcktCollisionProb[1][:],'-x', label="simulation, M=10")
        plt.title('Collision Probability of Finite-Station Slotted ALOHA')
        plt.xlabel('G (Offered Traffic)')
        plt.ylabel('Collision Prob')
##        G = np.array([np.arange(0,8+0.2,0.2)])
##        S = 1 - np.multiply(G,(1 - G / 10) ** (10 - 1)) - (1 - G / 10) ** (10)
##        plt.plot(G,S)
##        plt.plot(trafficOffered[2][:],pcktCollisionProb[2][:],'-s', label="simulation, M=25")
##        S = 1 - np.multiply(G,(1 - G / 25) ** (25 - 1)) - (1 - G / 25) ** (25)
##        plt.plot(G,S)
##        plt.plot(trafficOffered[3][:],pcktCollisionProb[3][:],'-o', label="simulation, M=50")
##        S = 1 - np.multiply(G,(1 - G / 50) ** (50 - 1)) - (1 - G / 50) ** (50)
##        plt.plot(G,S)
        plt.legend()
        plt.savefig('too.png')
        im = PIL.Image.open('too.png')
        button_image = customtkinter.CTkImage(im, size=(480, 320))
        self.label_collision_fig.configure(image=button_image, text= "")
        
        
    def exit_button_event(self):
        app.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()

export type IpFormData = {
    ip: string;
    detach: boolean;
};

export type PortData = {
    name: string;
    status: boolean;
};

export type DeviceData = {
    device: {
        status: string;
        model: string;
        ports: Array<PortData> | [];
    }
};

export type PortStatusProps = {
    devicePorts: Array<PortData>;
    deviceModel: string;
    formData: IpFormData;
};

export type DeviceProps = {
    deviceStatus: string;
    deviceModel: string;
    formData: IpFormData;
};

export type IndicationProps = {
    deviceStatus: string;
    deviceModel: string;
    formData: IpFormData;
};

export type IpFormProps = {
    pullFormData: (arg0: IpFormData) => void;
};